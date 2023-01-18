from fastapi import HTTPException
from loguru import logger
from string import Template
import pandas as pd
from typing import List
import yaml


def get_menu_page(config_doc, kod):
    if kod==1:
        return {'action':{'type':'alert','title':'Ошибка структуры','text':f'Не задана рабочая область kod:{kod}'}} 
    else:
        return get_template(config_doc, kod)        
        
    # if id == 1:  # Главная
    #     return {'action':{'type':'alert','title':'Ошибка структуры','text':'Не задана рабочая область'}} 
    # elif id == 201:  # Администрирование
    #     return {
    #         'type': 'tabs',
    #         'tabs': [
    #             {'kod': 20101, 'name': 'Режим', 'text': 'Пункт Режим'},
    #             {'kod': 20102, 'name': 'Настройки', 'text': 'Пункт Настройки'},
    #         ],
    #     }
    # elif id == 303:  # Прогнозирование
    #     return {'type': 'page', 'kod': 30301, 'text': 'Пункт Прогноз динамики'}
    # else:
    #     raise HTTPException(status_code=404, detail=f'Page {id} not found')


def get_template(config_doc, kod):
    lines = read_template('data/main_template.html')
    template = Template(''.join(lines))
    dct = config_doc['page-main']
    logger.debug(dct)
    template_str = template.substitute(dct)
    logger.debug(template_str)
    return template_str

def read_template(filename):
    with open(filename) as f:
        return f.readlines()

    

def get_menu(config_doc):
    ndn_map = extract_map(config_doc, 'dzgl')
    gag = get_gag_dzg(config_doc)

    df_graph = raw_graph_table(config_doc['graph'])
    df_graph['dn'] = df_graph.ndn.map(ndn_map).fillna(gag)
    df_graph['parent'] = df_graph.kod // 100

    df_graph = df_graph.loc[:, ['kod', 'parent', 'name', 'typ', 'dost']]
    df_graph['has_child'] = df_graph.kod.apply(lambda x: int(df_graph.parent.isin([x]).any()))
    # df_graph['breadcrumbs'] = df_graph.kod.apply(breadcrumbs, df_graph=df_graph)

    # action: {typ: 'alert',title,text} или action: {type:'page'}
    # df_graph['action'] = df_graph.has_child.map({0:'alert', 1:'page'})

    menus = df_graph[df_graph.typ.isin([1, 2])].loc[:, ['kod', 'parent', 'name', 'has_child']].to_dict('records')

    for menu in menus:
        if menu['has_child'] == 0:
            menu['action'] = {'type': 'alert', 'title':'Ошибка структуры','text':f"Не задана рабочая область kod:{menu['kod']}"}
        if menu['kod'] == 1:
            menu['action'] = {'type': 'page'}
        if menu['kod'] == 10:
            menu['action'] = {'type': 'alert', 'title':'Ошибка структуры','text':f"Не задана рабочая область kod:{menu['kod']}"}

        # elif menu['has_child'] == 1:
        #     menu['action'] = {'type': 'page'}
        # del menu['has_child']

    return menus
    # return df_graph[df_graph.typ.isin([1,2,3,4])]. \
    #     loc[:,['kod','parent','name','typ']].to_dict('records')
    # return df_graph[df_graph.typ.isin([1,2,3,4])]. \
    #     loc[:, ['kod', 'parent', 'name', 'dn', 'typ', 'dost']].to_dict(
    #     'records'
    # )


def read_config(filename: str = 'data/config.yml'):
    with open(filename) as f:
        return yaml.safe_load(f)


def extract_map(config_doc, name):
    return {int(k): str.strip(v) for k, v in [el.split(';') for el in config_doc[name]]}


def extract_bp_para_map(config_doc, name):
    return {
        int(k): (str.strip(v), str.strip(v1))
        for k, v, v1 in [el.split(';') for el in config_doc[name]]
    }


def raw_graph_table(graph: List[str]) -> pd.DataFrame:
    '''
    •	Код компонента (kod);
    •	Имя компонента (name)
    •	Тип компонента (typ);
    •	Тип доступа к компоненты (dost);
    •	Номер длинного имени (ndn).
    •	Тип длинного имени (tdn).
    • c7,c8,c9 резерв

    typ = Типы вершин:
       1 – Меню
       2 – СубМеню
       3 – Вкладка рабочей области (та же страница, но с «подзаголовком)
       4 – «обычная страница» (без вкладок в рабочей области)
       5 – прочие страницы (всплывающие окна сообщений, окошки help-ов и прочее)
    '''

    df = pd.DataFrame([row.split(';') for row in graph])
    df = df.applymap(str.strip)

    df.columns = pd.Index(['kod', 'name', 'typ', 'dost', 'ndn', 'tdn', 'c7', 'c8', 'c9'])
    df = df.astype(
        {
            'kod': 'int',
            'name': 'string',
            'typ': 'int',
            'dost': 'int',
            'ndn': 'int',
            'tdn': 'int',
            'c7': 'int',
            'c8': 'int',
            'c9': 'int',
        }
    )
    return df


def help_list(help_map, help_list):
    return [(h, help_map[h]) for h in help_list]


def knop_list(knop_map, group_map, knop_list, gag):
    groups = {}
    rows = [(int(str(h)[0]), h, knop_map.get(h, gag)) for h in knop_list]
    for row in rows:
        group_id = row[0] * 100
        if not group_map[group_id] in groups.keys():
            groups[group_map[group_id]] = []

        groups[group_map[group_id]].append({'kod': row[1], 'name': row[2][0], 'img': row[2][1]})

    return groups


# TODO
def get_gag_bp_para(config_doc):
    return ['Отсутствует описание Кнопки', 'gag-01.jpg']


# TODO
def get_gag_dzg(config_doc):
    # gag_zro: Заголовок страницы НЕ найден, страница все еще в стадии разработки
    return 'Заголовок страницы НЕ найден, страница все еще в стадии разработки'


def get_bp_niz(config_doc):
    gag = get_gag_bp_para(config_doc)
    bp_para_map = extract_bp_para_map(config_doc, 'bp-para')
    bp_group_map = extract_map(config_doc, 'bp-group')
    help_map = extract_map(config_doc, 'help1')

    niz_doc = config_doc['bp-niz']

    res = []
    for page_doc in niz_doc:
        page = page_doc['page']
        filtr = []
        help = help_list(help_map, page_doc['help'])
        knop = knop_list(bp_para_map, bp_group_map, page_doc['knop'], gag)
        res.append({'kod': page, 'help': help, 'group': knop, 'filtr': filtr})
    return res


def breadcrumbs(kod, df_graph):
    res = []
    while True:
        row = df_graph[df_graph.kod == kod]
        if row.empty:
            break
        kod = int(row.parent)
        res.append(row.name.iloc[0])
    return ' / '.join(res[::-1])
