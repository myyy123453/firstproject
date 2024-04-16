from django.core.cache import cache
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from tools.cache_dec import cache_set
from tools.logging_dec import logging_check, get_user_by_request
import json
from .models import Topic
from user.models import UserProfile
from message.models import Message

# 异常码 10300-10399

# Create your views here.
class TopicViews(View):
    # 清空缓存
    def clear_topics_caches(self, request):
        path = request.path_info
        cache_p = ['topics_cache_self_', 'cache_topics_']
        cache_h = ['', '?category=tec', '?category=no-tec']
        all_key = []
        for key_p in cache_p:
            for key_h in cache_h:
                all_key.append(key_p + path + key_h)
        print('clear chaches is ', all_key)
        cache.delete_many(all_key)

    def make_topic_res(self, author,author_topic, is_self):
        # {‘code’:200,’data’:{‘nickname’:’abc’, ’topics’:[{‘id’:1,’title’:’a’, ‘category’: ‘tec’, ‘created_time’: ‘2018-09-03 10:30:20’, ‘introduce’: ‘aaa’, ‘author’:’abc’}]}}

        if is_self:
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author).first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author).last()
        else:
            next_topic = Topic.objects.filter(id__gt=author_topic.id, author=author, limit='public').first()
            last_topic = Topic.objects.filter(id__lt=author_topic.id, author=author, limit='public').last()

        next_id = next_topic.id if next_topic else None
        last_id = last_topic.id if last_topic else None
        next_title = next_topic.title if next_topic else ''
        last_title = last_topic.title if last_topic else ''

        # 关联留言和回复
        all_message = Message.objects.filter(topic=author_topic).order_by('-created_time')

        msg_list = []  # 父级留言
        rep_idc = {}  # 子级留言
        m_count = 0
        for msg in all_message:
            if msg.parent_message:
                rep_idc.setdefault(msg.parent_message, [])
                rep_idc[msg.parent_message].append({'msg_id': msg.id, 'publisher': msg.publisher.nickname,
                                                    'publisher_avatr': str(msg.publisher.avatar),
                                                    'content': msg.content,
                                                    'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S')})
            else:
                m_count += 1
                msg_list.append({'id': msg.id, 'content': msg.content, 'publisher': msg.publisher.nickname,
                                 'publisher_avatar': str(msg.publisher.avatar),
                                 'created_time': msg.created_time.strftime('%Y-%m-%d %H:%M:%S'), 'reply': []})
        for m in msg_list:
            if m['id'] in rep_idc:
                m['reply'] = rep_idc[m['id']]

        res = {'code': 200, 'data': {}}
        res['data']['nickname'] = author.nickname
        res['data']['title'] = author_topic.title
        res['data']['category'] = author_topic.category
        res['data']['author_id'] = author_topic.author_id
        res['data']['created_time'] = author_topic.created_time.strftime('%Y-%m-%d %H:%M:%S')
        res['data']['content'] = author_topic.content
        res['data']['introduce'] = author_topic.introduce
        res['data']['author'] = author.nickname
        res['data']['last_id'] = last_id
        res['data']['last_title'] = last_title
        res['data']['next_id'] = next_id
        res['data']['next_title'] = next_title
        res['data']['messages'] = msg_list
        res['data']['messages_count'] = m_count
        return res
    def topics_res(self, author_topics):
        # {‘code’:200,’data’:{‘nickname’:’abc’, ’topics’:[{‘id’:1,’title’:’a’, ‘category’: ‘tec’, ‘created_time’: ‘2018-09-03 10:30:20’, ‘introduce’: ‘aaa’, ‘author’:’abc’}]}}
        res = {'code': 200, 'data': {}}
        topics_res = []
        for topic in author_topics:
            d = {}
            d['id'] = topic.id
            d['title'] = topic.title
            d['category'] = topic.category
            # d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
            d['created_time'] = topic.created_time
            d['introduce'] = topic.introduce
            d['author'] = topic.author_id
            topics_res.append(d)

        res['data']['topics'] = topics_res
        res['data']['nickname'] = topic.author_id
        return res
    def make_topics_res(self, author, author_topics):
        # {‘code’:200,’data’:{‘nickname’:’abc’, ’topics’:[{‘id’:1,’title’:’a’, ‘category’: ‘tec’, ‘created_time’: ‘2018-09-03 10:30:20’, ‘introduce’: ‘aaa’, ‘author’:’abc’}]}}
        res = {'code': 200, 'data': {}}
        topics_res = []
        for topic in author_topics:
            d = {}
            d['id'] = topic.id
            d['title'] = topic.title
            d['category'] = topic.category
            # d['created_time'] = topic.created_time.strftime("%Y-%m-%d %H:%M:%S")
            d['created_time'] = topic.created_time
            d['introduce'] = topic.introduce
            d['author'] = author.nickname
            topics_res.append(d)

        res['data']['topics'] = topics_res
        res['data']['nickname'] = author.nickname
        return res

    @method_decorator(logging_check)
    def post(self, request, author_id):
        # {"content":"<p><span style=\"font-weight: bold;\">heiheihei</span><br></p>","content_text":"heiheihei","limit":"public","title":"hahahaha","category":"tec"}
        author = request.myuser
        # 取出前端数据
        json_str = request.body
        json_obj = json.loads(json_str)
        title = json_obj['title']
        content = json_obj['content']
        content_text = json_obj['content_text']
        introduce = content_text[:30]
        limit = json_obj['limit']
        category = json_obj['category']
        if limit not in ['public', 'private']:
            result = {'code': 10300, 'error': 'The limit error~'}
            return JsonResponse(result)

        # 创建topic数据
        Topic.objects.create(title=title, content=content, limit=limit, category=category, introduce=introduce,
                             author=author)

        # 删除缓存
        self.clear_topics_caches(request)

        return JsonResponse({'code': 200})

    @method_decorator(cache_set(300))
    def get(self, request, author_id):

        # 访问者 visitor
        # 当前被访问博客的博主 author
        try:
            author = UserProfile.objects.get(username=author_id)
        except Exception as e:
            result = {'code': 10301, 'error': 'The author is not existed'}
            return JsonResponse(result)

        visitor = get_user_by_request(request)
        visitor_username = None
        if visitor:
            visitor_username = visitor.username
        t_id = request.GET.get('t_id')
        if t_id:
            t_id = int(t_id)
            is_self = False
            if visitor_username == author_id:
                is_self = True
                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id)
                except Exception  as e:
                    result = {'code': 10302, 'error': 'No Topic'}
                    return JsonResponse(result)
            else:
                try:
                    author_topic = Topic.objects.get(id=t_id, author_id=author_id, limit='public')
                except Exception  as e:
                    result = {'code': 10302, 'error': 'No Topic'}
                    return JsonResponse(result)
            res = self.make_topic_res(author, author_topic, is_self)
            return JsonResponse(res)
        else:
            category = request.GET.get('category')

            if category in ['tec', 'no-tec']:

                if visitor_username == author_id:
                    # 博主访问自己博客
                    author_topic = Topic.objects.filter(author_id=author_id, category=category)
                else:
                    author_topic = Topic.objects.filter(author_id=author_id, limit='public', category=category)
            else:
                if visitor_username == author_id:
                    # 博主访问自己博客
                    author_topic = Topic.objects.filter(author_id=author_id)
                else:
                    author_topic = Topic.objects.filter(author_id=author_id, limit='public')

            res = self.make_topics_res(author, author_topic)
            return JsonResponse(res)
    @method_decorator(cache_set(300))
    def put(self, request):
        # 访问者 visitor
        # visitor = get_user_by_request(request)
        # visitor_username = None
        # if visitor:
        #     visitor_username = visitor.username
        t_id = request.GET.get('t_id')
        topic = Topic.objects.filter(limit='public')
        res = self.topics_res(author_topics=topic)
        return JsonResponse(res)