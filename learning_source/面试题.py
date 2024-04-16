# @Author : Kql
# @Time : 2023/6/27 16:09
# 小学春游 - 两组同学，每组1-3人，每组有一个队长;春游期间，由于景点人数较多，秩序混乱，班主任要求在指定地点，按组集合

# 源数据
s = [{'name': 'leader-1', 'belong_to': None}, {'name': 'jack', 'belong_to': 'leader-2'},
     {'name': 'lili', 'belong_to': 'leader-1'}, {'name': 'leader-2', 'belong_to': None},
     {'name': 'Tom', 'belong_to': 'leader-1'}]
# 目标数据
d = [
    {'name': 'leader-1', 'team': [{'name': 'lili'}, {'name': 'Tom'}]},
    {'name': 'leader-2', 'team': [{'name': 'jack'}]}
]


def find_team(data):
    leader_list = []
    s_dict = {}
    for dic in data:
        if dic['belong_to']:
            # 队员，如果s_dict存在所在组，则更新，否则就新增一个组 {'leader-1':[{'name':'jack'}]}
            s_dict.setdefault(dic['belong_to'], [])
            s_dict[dic['belong_to']].append({'name': dic['name']})
        else:
            # 队长，将队长数据构造成一个 {'name':'leader-1','team':[]} 格式
            leader_list.append({'name': dic['name'], 'team': []})
        # 循环遍历队长数据，如果存在，则将对应队长的数据添加到leader_list中
        for te in leader_list:
            if te['name'] in s_dict:
                te['team'] = s_dict[te['name']]
    return leader_list


if __name__ == '__main__':
    res = find_team(data=s)
    print(res)
