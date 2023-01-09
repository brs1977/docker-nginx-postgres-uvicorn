from app.db.session import metadata
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Table,
)

users_table = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(40), unique=True, index=True, nullable=False),
    Column("username", String(32), unique=True, index=True, nullable=False),
    Column("fio", String(100), nullable=False),
    Column("password", String(256), nullable=False),
    Column(
        "is_active",
        Boolean(),
        server_default=sqlalchemy.sql.expression.true(),
        nullable=False,
    ),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

roles_table = sqlalchemy.Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(32), unique=True, nullable=False),
)


structure_formations_table = Table(
    "structure_formations",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("pid", Integer),
    Column("name", String(32)),
)


s_posled_table = Table(
    "s_posled",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    comment='Справочник "Уровни тяжести последствий событий"',
)
s_sobytiya_table = Table(
    "s_sobytiya",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Аббрев."),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("code_posled", Integer, nullable=False, doc="Код тяжести"),
    Column(
        "name",
        String(255),
        nullable=False,
        doc="Наименование категории, вида и типа событий",
    ),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    comment='Справочник "Классификация событий"',
)
s_faktor_table = Table(
    "s_faktor",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД группы"),
    comment='Справочник "Группы опасных факторов"',
)
k_podgr_table = Table(
    "k_podgr",
    metadata,
    Column(
        "short_name",
        String(50),
        nullable=False,
        doc="Сокращенно для экр. форм и печати",
    ),
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД подгруппы"),
    Column(
        "s_faktor_id",
        Integer,
        ForeignKey("s_faktor.id"),
        nullable=False,
        doc="ИД группы",
    ),
    Column("name", String(255), nullable=False, doc="Наименование подгруппы"),
    comment='Классификатор "Подгруппы причин"',
)
k_prichiny_table = Table(
    "k_prichiny",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Обозначение (в документах)"),
    Column("name", String(255), nullable=False, doc="Наименование пункта подгруппы"),
    Column("k_podgr_id", Integer, primary_key=True, nullable=False, doc="ИД подгруппы"),
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД причины"),
    comment='Классификатор "Причины событий"',
)
s_deyatelnost_table = Table(
    "s_deyatelnost",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование пункта подгруппы"),
    Column(
        "parent_id",
        Integer,
        ForeignKey("s_deyatelnost.id"),
        nullable=False,
        doc="Пред уровень код",
    ),
    comment='Справочник "Виды деятельности и обеспечения при производстве полетов"',
)
k_tip_vs_table = Table(
    "k_tip_vs",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    comment="Типы воздушных судов. Структура классификатора",
)
s_naznach_vs_table = Table(
    "s_naznach_vs",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Назначение ВС"',
)
s_roda_table = Table(
    "s_roda",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Рода авиации"',
)
t_org_struct_table = Table(
    "t_org_struct",
    metadata,
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    comment='Таблица "Организационная структура авиационной системы"',
)
t_vs_chasti_table = Table(
    "t_vs_chasti",
    metadata,
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    comment='Связанная таблица "Воздушные суда части"',
)
s_uprav_table = Table(
    "s_uprav",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Уровни управления"',
)
s_strateg_uprav_table = Table(
    "s_strateg_uprav",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Формирования оперативно-стратегического уровня управления"',
)
s_operativ_uprav_table = Table(
    "s_operativ_uprav",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    comment='Справочник "Формирования оперативного уровня управления"',
)
s_foiv_table = Table(
    "s_foiv",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    comment='Справочник "Федеральные органы исполнительной власти (ФОИВ)"',
)
k_aerodrom_table = Table(
    "k_aerodrom",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    comment='Классификатор "Аэродромы базирования"',
)
t_aerodrom_table = Table(
    "t_aerodrom",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    comment='Таблица базы данных "Готовность аэродромов"',
)
s_aerodrom_table = Table(
    "s_aerodrom",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    comment='Справочник "Готовность аэродрома"',
)
s_ogranich_table = Table(
    "s_ogranich",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment='Справочник "Причины ограничений"',
)
t_meteo_table = Table(
    "t_meteo",
    metadata,
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    comment='Таблица "Прогноз метеообстановки на аэродроме"',
)
s_pogoda_table = Table(
    "s_pogoda",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment='Справочник "Соответствие прогноза погоды"',
)
s_vidimost_table = Table(
    "s_vidimost",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment='Справочник "Явления, ухудшающие видимость"',
)
s_osadki_table = Table(
    "s_osadki",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment='Справочник "Виды осадков"',
)
s_vetrov_yavl_table = Table(
    "s_vetrov_yavl",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Вид ветровых явлений"',
)
s_oblachnost_table = Table(
    "s_oblachnost",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment='Справочник "Виды облачности"',
)
s_osveshennost_table = Table(
    "s_osveshennost",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Вариант освещенности"',
)
s_meteousloviya_table = Table(
    "s_meteousloviya",
    metadata,
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    comment='Справочник "Варианты метеоусловий"',
)
s_letnye_smeni_table = Table(
    "s_letnye_smeni",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    Column("code", Integer, nullable=False, doc="Код"),
    comment='Справочник "Варианты летных смен"',
)
t_plan_letnyh_smen_table = Table(
    "t_plan_letnyh_smen",
    metadata,
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    comment='Таблица базы данных "Планирование и выполнение летных смен"',
)
t_narusheniya_letnyh_smen_table = Table(
    "t_narusheniya_letnyh_smen",
    metadata,
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    comment='Таблица базы данных "Нарушения и недостатки при проведении летных смен"',
)
t_uchet_sobytij_table = Table(
    "t_uchet_sobytij",
    metadata,
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    comment="""Таблица базы данных "Учет авиационных событий """
    """по подгруппам факторов, за периоды времени""",
)
s_period_ucheta_table = Table(
    "s_period_ucheta",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment='Справочник "Кодирование периодов учета"',
)
t_itog_vs_table = Table(
    "t_itog_vs",
    metadata,
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    comment='Таблица базы данных "Итоги летной деятельности, за периоды времени по всем типам ВС"',
)
t_poteri_table = Table(
    "t_poteri",
    metadata,
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    comment='Таблица базы данных "Потери в результате авиационных событий, за периоды времени"',
)
t_poteri_vs_table = Table(
    "t_poteri_vs",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    comment='Таблица базы данных "Потери ВС по типам по периодам времени"',
)
t_bezopasnost_table = Table(
    "t_bezopasnost",
    metadata,
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    comment='Таблица базы данных "Показатели безопасности полетов за период времени"',
)
t_uroven_ls_table = Table(
    "t_uroven_ls",
    metadata,
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    comment='Таблица базы данных "Квалификация и уровень подготовки летного состава (летчики)"',
)
t_ispravnost_vs_table = Table(
    "t_ispravnost_vs",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    comment='Таблица базы данных "Состояние исправности ВС"',
)
t_uchet_posled_table = Table(
    "t_uchet_posled",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    comment='Таблица базы данных "Оперативный учет авиационных событий и их последствий"',
)
t_uchet_poter_vs_table = Table(
    "t_uchet_poter_vs",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    comment='Таблица базы данных данных "Оперативный учет потерь и повреждений ВС по типам"',
)
t_nedostatki_table = Table(
    "t_nedostatki",
    metadata,
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    comment='Таблица базы данных данных "Количество нарушений и недостатков по периодам времени"',
)
s_itog_vs_tip_table = Table(
    "s_itog_vs_tip",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("format", String(255), nullable=False, doc="Формат"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    comment="""Таблица базы данных данных "Итоги летной деятельности"""
    """, за периоды времени по типам ВС""",
)
t_nalet_vs_table = Table(
    "t_nalet_vs",
    metadata,
    Column("name", String(255), nullable=False, doc="Наименование поля"),
    Column("prim", String(500), nullable=False, doc="Примечание"),
    Column("format", String(255), nullable=False, doc="Формат"),
    comment='Таблица базы данных данных "Учет налета ВС и экипаже по типам ВС"',
)
