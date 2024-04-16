import csv
from _decimal import Decimal
from datetime import datetime
from pyexpat.errors import messages
from venv import logger

from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render
from dns import transaction


def common_utils_md5_sign_str(unsign_str):
    pass


@user_passes_test(lambda u: u.is_superuser)
@login_required
@transaction.atomic
def up_fundrecord_by_csv(request):
    """
    卡片流水记录处理函数
    """
    # 未录入卡片
    not_import_vcards = []

    # 处理条数
    suc = 0
    repeat = 0
    fail = 0

    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)

        if form.is_valid():
            # 处理上传的文件
            uploaded_file = request.FILES['csvfile']
            if uploaded_file.name.endswith('.csv'):
                csv_data = uploaded_file.read().decode('utf-8')
                lines = csv_data.splitlines()
                reader = csv.reader(lines)

                # 跳过表头
                next(reader)

                # 遍历处理
                for row in reader:
                    # transid
                    vcard = VirtualCard.objects.filter(
                        card_transid=row[0]).first()

                    if vcard:
                        # 消费类型
                        if row[2] == 'Authorization(Purchase)':
                            record_type = 4
                        else:
                            record_type = 2

                        # 时间
                        auth_at = row[7]
                        # 金额
                        amount = Decimal(row[11])

                        datetime_obj = datetime.strptime(
                            auth_at, '%Y-%m-%d %H:%M:%S')
                        timestamp = datetime_obj.timestamp()

                        unsign_str = str(amount) + vcard.currency + \
                                     str(int(timestamp)) + vcard.card_transid
                        md5str = common_utils_md5_sign_str(unsign_str)

                        # 避免重复录入
                        fundrecord = FundRecord.objects.filter(
                            record_md5=md5str).first()

                        if fundrecord:
                            repeat += 1
                        else:
                            # 新增卡片消费记录
                            try:
                                with transaction.atomic():
                                    # 交易状态为成功
                                    if row[3] == 'Success':
                                        # 卡片流水记录
                                        fund_record = FundRecord.objects.create(
                                            card=vcard,
                                            record_md5=md5str,
                                            record_type=record_type,
                                            amount=amount,
                                            pos_currency=row[8],
                                            pos_amount=row[9],
                                            auth_at=auth_at,
                                            status=1,
                                        )

                                        # 修改卡片余额
                                        if int(record_type) == 4:
                                            vcard.settlement_amount += amount
                                            vcard.remaining_amount -= amount
                                        elif int(record_type) == 2:
                                            vcard.settlement_amount -= amount
                                            vcard.remaining_amount += amount
                                        vcard.save()

                                    else:
                                        fund_record = FundRecord.objects.create(
                                            card=vcard,
                                            record_md5=md5str,
                                            record_type=record_type,
                                            amount=amount,
                                            pos_currency=row[8],
                                            pos_amount=row[9],
                                            auth_at=auth_at,
                                            resmsg=row[5],
                                            status=2,
                                        )

                                    # 记录处理成功
                                    suc += 1

                            except Exception as e:
                                fail += 1
                                logger.debug(e)

                    else:
                        not_import_vcards.append((row[0], row[1]))

            else:
                messages.error(request, '文件格式错误！')

        if fail > 0:
            messages.warning(
                request, '成功{}条,重复{}条,失败{}条'.format(
                    suc, repeat, fail))
        else:
            messages.success(request, '成功{}条,重复{}条'.format(suc, repeat, fail))
    else:
        form = MyForm()

    content = {
        'title': '文件上传',
        'form': form,
        'not_import_vcards': list(set(not_import_vcards)),
        'suc': suc,
        'fail': fail,
    }

    return render(request, 'admin/fundrecord_up.html', content)
