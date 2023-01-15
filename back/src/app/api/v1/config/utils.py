import pandas as pd
import yaml


def get_menu(config_doc):
    ndn_map = extract_map(config_doc, "dzgl")
    gag = get_gag_dzg(config_doc)

    df_graph = raw_graph_table(config_doc["graph"])
    df_graph["dn"] = df_graph.ndn.map(ndn_map).fillna(gag)
    df_graph["parent"] = df_graph.kod // 100

    # return df_graph[df_graph.typ.isin([1,2])].loc[:,['kod','parent','name']].to_dict('records')
    return df_graph.loc[:, ["kod", "parent", "name", "dn", "typ", "dost"]].to_dict(
        "records"
    )


def read_config(filename: str = "data/config.yml"):
    with open(filename) as f:
        return yaml.safe_load(f)


def extract_map(config_doc, name):
    return {int(k): str.strip(v) for k, v in [el.split(";") for el in config_doc[name]]}


def extract_bp_para_map(config_doc, name):
    return {
        int(k): (str.strip(v), str.strip(v1))
        for k, v, v1 in [el.split(";") for el in config_doc[name]]
    }


def raw_graph_table(graph: list[str]) -> pd.DataFrame:
    """
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
    """

    df = pd.DataFrame([row.split(";") for row in graph])
    df = df.applymap(str.strip)

    df.columns = pd.Index(
        ["kod", "name", "typ", "dost", "ndn", "tdn", "c7", "c8", "c9"]
    )
    df = df.astype(
        {
            "kod": "int",
            "name": "string",
            "typ": "int",
            "dost": "int",
            "ndn": "int",
            "tdn": "int",
            "c7": "int",
            "c8": "int",
            "c9": "int",
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

        groups[group_map[group_id]].append(
            {"kod": row[1], "name": row[2][0], "img": row[2][1]}
        )

    return groups


# TODO
def get_gag_bp_para(config_doc):
    return ["Отсутствует описание Кнопки", "gag-01.jpg"]


# TODO
def get_gag_dzg(config_doc):
    # gag_zro: Заголовок страницы НЕ найден, страница все еще в стадии разработки
    return "Заголовок страницы НЕ найден, страница все еще в стадии разработки"


def get_bp_niz(config_doc):
    gag = get_gag_bp_para(config_doc)
    bp_para_map = extract_bp_para_map(config_doc, "bp-para")
    bp_group_map = extract_map(config_doc, "bp-group")
    help_map = extract_map(config_doc, "help1")

    niz_doc = config_doc["bp-niz"]

    res = []
    for page_doc in niz_doc:
        page = page_doc["page"]
        filtr = []
        help = help_list(help_map, page_doc["help"])
        knop = knop_list(bp_para_map, bp_group_map, page_doc["knop"], gag)
        res.append({"kod": page, "help": help, "group": knop, "filtr": filtr})
    return res
