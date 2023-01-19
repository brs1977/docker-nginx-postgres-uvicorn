from app.db.session import metadata
import sqlalchemy
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Time,
    Date,
    Numeric,
    DateTime,
    BOOLEAN,
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
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("kod", Integer, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Уровни  тяжести  последствий  событий»",
)

s_sobytiya_table = Table(
    "s_sobytiya",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("kod", Integer, nullable=False, doc="Код"),
    Column("kod_posled", Integer, nullable=False, doc="Код  тяжести"),
    Column(
        "name", String(255), nullable=False, doc="Наименование  категории,  вида  и  типа  событий"
    ),
    Column("short_name", String(50), nullable=False, doc="Аббрев."),
    comment="Справочник  «Классификация  событий»",
)

s_faktor_table = Table(
    "s_faktor",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД  группы"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment="Справочник  «Группы  опасных  факторов»",
)

k_podgr_table = Table(
    "k_podgr",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД  подгруппы"),
    Column("name", String(255), nullable=False, doc="Наименование  подгруппы"),
    Column("s_faktor_id", Integer, ForeignKey("s_faktor.id"), nullable=False, doc="ИД  группы"),
    Column("short_name", String(50), nullable=False, doc="Сокращенно  для  экр.  форм  и  печати"),
    comment="Классификатор  «Подгруппы  причин»",
)

k_prichiny_table = Table(
    "k_prichiny",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД  причины"),
    Column("k_podgr_id", Integer, ForeignKey("k_podgr.id"), nullable=False, doc="ИД  подгруппы"),
    Column("name", String(255), nullable=False, doc="Наименование  пункта  подгруппы"),
    Column("short_name", String(50), nullable=False, doc="Обозначение  (в  документах)"),
    comment="Классификатор  «Причины  событий»",
)

s_deyatelnost_table = Table(
    "s_deyatelnost",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column("name", String(255), nullable=False, doc="Наименование  пункта  подгруппы"),
    Column(
        "parent_id",
        Integer,
        ForeignKey("s_deyatelnost.id"),
        nullable=False,
        doc="Пред  уровень  код",
    ),
    comment="Справочник  «Виды  деятельности  и  обеспечения  при  производстве  полетов»",
)

k_tip_vs_table = Table(
    "k_tip_vs",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="Код"),
    Column(
        "kod_vs",
        Integer,
        nullable=False,
        doc="Код  типа  ВС  в  автоматизированной  системе  «Надежность»",
    ),
    Column("modif", String(255), nullable=False, doc="модификация"),
    Column("name", String(255), nullable=False, doc="Кодирование  типа  ВС"),
    Column("nomer", Integer, nullable=False, doc="номер"),
    Column("parent_id", Integer, ForeignKey("k_tip_vs.id"), nullable=False, doc="базовый  тип"),
    Column("priznak_vs", Integer, nullable=False, doc="Признак  ВС"),
    Column(
        "s_naznach_vs_id", Integer, ForeignKey("k_tip_vs.id"), nullable=False, doc="Назначение  ВС"
    ),
    comment="Типы  воздушных  судов.  Структура  классификатора",
)

s_naznach_vs_table = Table(
    "s_naznach_vs",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Назначение  ВС»",
)

s_roda_table = Table(
    "s_roda",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Рода  авиации»",
)

t_org_struct_table = Table(
    "t_org_struct",
    metadata,
    Column(
        "chast", String(255), nullable=False, doc="Действительное  наименование  части  сокращенно"
    ),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "index_chasti",
        Integer,
        nullable=False,
        doc="Индекс  части  (уникальный  10-значный  код,  присваиваемый  в  директиве  НГШ  ВС    о  формировании  части)",
    ),
    Column(
        "k_aerodrom_id",
        Integer,
        ForeignKey("k_aerodrom.id"),
        nullable=True,
        doc="Код  аэродрома  базирования  (если  есть)",
    ),
    Column(
        "kod_okrug",
        Integer,
        nullable=True,
        doc="Код  военного  округа,  на  территории  которого  дислоцируется  войсковая  часть",
    ),
    Column("mesto", String(255), nullable=True, doc="Наименование  места  дислокации"),
    Column("ospd_adr", String(255), nullable=True, doc="Адрес  в  ОСПД"),
    Column(
        "parent_id",
        Integer,
        ForeignKey("t_org_struct.id"),
        nullable=False,
        doc="Индекс  подчиненности  (ИД  записи  непосредственного  начальника)",
    ),
    Column("poch_adr", String(255), nullable=True, doc="Почтовый  адрес"),
    Column("poch_index", String(255), nullable=True, doc="Почтовый  индекс"),
    Column(
        "s_uprav_id",
        Integer,
        ForeignKey("s_uprav.id"),
        nullable=False,
        doc="Код  принадлежности  к  уровню  управления",
    ),
    Column("usl_vch", String(255), nullable=False, doc="Условное  наименование  (в/ч)"),
    Column(
        "vch",
        String(255),
        nullable=True,
        doc="Литерное  наименование  в/части  (организации)  полное",
    ),
    Column(
        "vch_name",
        String(255),
        nullable=True,
        doc="Литерное  наименование  в/части  (организации)  полное",
    ),
    Column(
        "vch_short_name",
        String(255),
        nullable=True,
        doc="Литерное  наименование  в/части  (организации)  сокращенно",
    ),
    Column("zspd_adr", String(255), nullable=True, doc="Адрес  в  ЗСПД"),
    comment="Таблица  «Организационная  структура  авиационной  системы»",
)

t_vs_chasti_table = Table(
    "t_vs_chasti",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="ИД  части  в  оргструктуре"),
    Column("kod", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("shtat", Integer, nullable=False, doc="Количество  по  штату"),
    Column("spisok", Integer, nullable=False, doc="Количество  по  списку"),
    comment="Связанная  таблица  «Воздушные  суда  части»",
)

s_uprav_table = Table(
    "s_uprav",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment="Справочник  «Уровни  управления»",
)

s_strateg_uprav_table = Table(
    "s_strateg_uprav",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Формирования  оперативно-стратегического  уровня  управления»",
)

s_operativ_uprav_table = Table(
    "s_operativ_uprav",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Формирования  оперативного  уровня  управления»",
)

s_foiv_table = Table(
    "s_foiv",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Федеральные  органы  исполнительной  власти  (ФОИВ)»",
)

k_aerodrom_table = Table(
    "k_aerodrom",
    metadata,
    Column("dolgota", String(255), nullable=False, doc="Долгота  контрольной  точки  аэродрома"),
    Column("foiv", Integer, nullable=False, doc="Код  принадлежности  ФОИВ"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("index_aero", String(255), nullable=False, doc="Индекс  аэродрома"),
    Column("index_mezhd", String(255), nullable=False, doc="Индекс  международный"),
    Column("index_ros", String(255), nullable=False, doc="Индекс  российский"),
    Column(
        "index_voen",
        Integer,
        nullable=True,
        doc="Индекс  воинской  части,  командир  которой  назначен  старшим  авиационным  начальником  на  аэродроме",
    ),
    Column(
        "klas_grazhd",
        String(1),
        nullable=True,
        doc="Класс  аэродрома  (гражданская  классификация)	А/Б/В/Г/Д/Е/null",
    ),
    Column(
        "klas_voen",
        Integer,
        nullable=True,
        doc="Класс  аэродрома  (военная  классификация)	0  /  1  /  2  /  3  /  null",
    ),
    Column(
        "kod_ogran",
        Integer,
        ForeignKey("s_ogranich.id"),
        nullable=False,
        doc="Код  причины  ограничения  функционирования",
    ),
    Column("kod_okrug", Integer, nullable=False, doc="Код  Федерального  округа"),
    Column("name", String(255), nullable=False, doc="Наименование  аэродрома"),
    Column(
        "s_strateg_uprav_1_id",
        Integer,
        ForeignKey("s_strateg_uprav.id"),
        nullable=False,
        doc="Код  принадлежности_1",
    ),
    Column(
        "s_strateg_uprav_2_id",
        Integer,
        ForeignKey("s_strateg_uprav.id"),
        nullable=False,
        doc="Код  принадлежности_2",
    ),
    Column(
        "shirota",
        String(255),
        nullable=False,
        doc="Широта  контрольной  точки  аэродрома	координаты",
    ),
    Column(
        "sovmets_isp",
        Integer,
        nullable=False,
        doc="Признак  совместного  пользования  аэродромом  (нет/совм.  базир/совм.  использ)	0  /  1  /  2",
    ),
    comment="Классификатор  «Аэродромы  базирования»",
)

t_aerodrom_table = Table(
    "t_aerodrom",
    metadata,
    Column("data", DateTime, nullable=False, doc="Дата"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "k_aerodrom_id", Integer, ForeignKey("k_aerodrom.id"), nullable=False, doc="ИД  аэродрома"
    ),
    Column("konesh", Time, nullable=False, doc="Время  конечное"),
    Column("nash", Time, nullable=False, doc="Время  начальное"),
    Column(
        "s_aerodrom_id",
        Integer,
        ForeignKey("s_aerodrom.id"),
        nullable=False,
        doc="Код  готовности  аэродрома",
    ),
    Column(
        "s_ogranich_id",
        Integer,
        ForeignKey("s_ogranich.id"),
        nullable=False,
        doc="Код  причины  ограничений",
    ),
    comment="Таблица  базы  данных  «Готовность  аэродромов»",
)

s_aerodrom_table = Table(
    "s_aerodrom",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Готовность  аэродрома»",
)

s_ogranich_table = Table(
    "s_ogranich",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Причины  ограничений»",
)

t_meteo_table = Table(
    "t_meteo",
    metadata,
    Column("data", DateTime, nullable=False, doc="Прогноз  на  дату"),
    Column("davlenie", Integer, nullable=False, doc="Атмосферное  давление"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "k_aerodrom_id", Integer, ForeignKey("k_aerodrom.id"), nullable=False, doc="ИД  аэродрома"
    ),
    Column("napr_vetra", Integer, nullable=False, doc="Направление  ветра,  градусы"),
    Column("ngo", Integer, nullable=False, doc="Нижняя  граница  (НГО),  (м)"),
    Column("oblachnost", Integer, nullable=False, doc="Облачность,  баллы"),
    Column("osadki", Integer, nullable=False, doc="Количество  осадков  (мм)"),
    Column(
        "s_oblachnost_id",
        Integer,
        ForeignKey("s_oblachnost.id"),
        nullable=False,
        doc="Тип  облачности  ",
    ),
    Column(
        "s_osadki_id", Integer, ForeignKey("s_osadki.id"), nullable=False, doc="Осадки,  код	целое"
    ),
    Column(
        "s_vetrov_yavl_id",
        Integer,
        ForeignKey("s_vetrov_yavl.id"),
        nullable=False,
        doc="Ветровые  явления,  код	целое",
    ),
    Column(
        "s_vidimost_id",
        Integer,
        ForeignKey("s_vidimost.id"),
        nullable=False,
        doc="Ухудшение  видимости,  код",
    ),
    Column("skorost_vetra_max", Integer, nullable=False, doc="Скорость  ветра  макс  (м/сек)"),
    Column("skorost_vetra_min", Integer, nullable=False, doc="Скорость  ветра  мин  (м/сек)"),
    Column("temp_max", Integer, nullable=False, doc="Температура  макс,  градусы  С"),
    Column("temp_min", Integer, nullable=False, doc="Температура  мин,  градусы  С"),
    Column("vgo", Integer, nullable=False, doc="Верхняя  граница  (ВГО),  (м)"),
    Column("vid_gor", Numeric(12, 2), nullable=False, doc="Посадочная  видимость  гор"),
    Column("vid_vert", Integer, nullable=False, doc="Посадочная  видимость  верт  (м)"),
    Column("vlazhnost", Integer, nullable=False, doc="Влажность"),
    comment="Таблица  «Прогноз  метеообстановки  на  аэродроме»",
)

s_pogoda_table = Table(
    "s_pogoda",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment="Справочник  «Соответствие  прогноза  погоды»",
)

s_vidimost_table = Table(
    "s_vidimost",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Явления,  ухудшающие  видимость»",
)

s_osadki_table = Table(
    "s_osadki",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Виды  осадков»",
)

s_vetrov_yavl_table = Table(
    "s_vetrov_yavl",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Вид  ветровых  явлений»",
)

s_oblachnost_table = Table(
    "s_oblachnost",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Виды  облачности»",
)

s_osveshennost_table = Table(
    "s_osveshennost",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Вариант  освещенности»",
)

s_meteousloviya_table = Table(
    "s_meteousloviya",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Варианты  метеоусловий»",
)

s_letnye_smeni_table = Table(
    "s_letnye_smeni",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    Column("short_name", String(50), nullable=False, doc="Сокращение"),
    comment="Справочник  «Варианты  летных  смен»",
)

t_plan_letnyh_smen_table = Table(
    "t_plan_letnyh_smen",
    metadata,
    Column("aerodrom", Integer, nullable=False, doc="Идентификатор  аэродрома"),
    Column("avia_sobit", BOOLEAN, nullable=False, doc="Признак  наличия  авиационного  события"),
    Column("chast", Integer, nullable=False, doc="Идентификатор  части"),
    Column("data", DateTime, nullable=False, doc="Дата  начала  летной  смены"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("kod_meteo", Integer, nullable=False, doc="Код  варианта  метеоусловий	целое"),
    Column("kod_smeni", Integer, nullable=False, doc="Код  варианта  летной  смены"),
    Column(
        "kod_vypoln",
        Integer,
        nullable=False,
        doc="Код  выполнения  (при  формировании  донесения  -  выпадающий  список)	0/1/2	0  –  выполнена  1  –  отменена  2  –  прекращена  досрочно",
    ),
    Column("nalet", DateTime, nullable=False, doc="Налет  ВС"),
    Column("nalet_den", Integer, nullable=False, doc="Налет  ВС  днем"),
    Column("nalet_dpmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДПМУ"),
    Column("nalet_dsmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДСМУ"),
    Column("nalet_ncmu", DateTime, nullable=False, doc="Налет  экипажей  в  НСМУ"),
    Column("nalet_noch", Integer, nullable=False, doc="Налет  ВС  ночью"),
    Column("nalet_npmu", DateTime, nullable=False, doc="Налет  экипажей  в  НПМУ"),
    Column(
        "podrazd",
        String(8),
        nullable=False,
        doc="Подразделение,  выполняющее  полеты	Текст  (8  симв)	1аэ  /  2аэ  /3аэ  /  ап/  1аэ,  3аэ",
    ),
    Column("polet", Integer, nullable=False, doc="Количество  полетов  ВС"),
    Column("polet_den", Integer, nullable=False, doc="Количество  полетов  ВС  днем"),
    Column("polet_noch", Integer, nullable=False, doc="Количество  полетов  ВС  ночью"),
    Column("prognoz", Integer, nullable=False, doc="Код  соответствия  прогноза  погоды"),
    comment="Таблица  базы  данных  «Планирование  и  выполнение  летных  смен»",
)

t_narusheniya_letnyh_smen_table = Table(
    "t_narusheniya_letnyh_smen",
    metadata,
    Column("aerodrom", Integer, nullable=False, doc="Идентификатор  аэродрома"),
    Column("chast", Integer, nullable=False, doc="Идентификатор  части"),
    Column("data", DateTime, nullable=False, doc="Дата  начала  летной  смены"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("massiv", Integer[24][3], nullable=False, doc="данные"),
    comment="Таблица  базы  данных  «Нарушения  и  недостатки  при  проведении  летных  смен»",
)

t_uchet_sobytij_table = Table(
    "t_uchet_sobytij",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("massiv", Integer[13][11], nullable=False, doc="данные"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    comment="Таблица  базы  данных  «Учет  авиационных  событий  по  подгруппам  факторов,  за  периоды  времени»",
)

s_period_ucheta_table = Table(
    "s_period_ucheta",
    metadata,
    Column("code", Integer, nullable=False, doc="Код"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("name", String(255), nullable=False, doc="Наименование"),
    comment="Справочник  «Кодирование  периодов  учета»",
)

t_itog_vs_table = Table(
    "t_itog_vs",
    metadata,
    Column("dosroch", Integer, nullable=False, doc="Из  них  прекращено  досрочно"),
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("kol_den", Integer, nullable=False, doc="Количество  дневных  летных  смен  (Д)"),
    Column("kol_noch", Integer, nullable=False, doc="Количество  ночных  летных  смен  (Н)"),
    Column(
        "kol_prognoz",
        Integer,
        nullable=False,
        doc="Количество  оправдавшихся  метеопрогнозов	целое",
    ),
    Column("kol_smesh", Integer, nullable=False, doc="Количество  смешанных  летных  смен  (ДН)"),
    Column("nalet", DateTime, nullable=False, doc="Налет  ВС"),
    Column("nalet_den", Integer, nullable=False, doc="Налет  ВС  днем"),
    Column("nalet_dpmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДПМУ"),
    Column("nalet_dsmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДСМУ"),
    Column("nalet_ncmu", DateTime, nullable=False, doc="Налет  экипажей  в  НСМУ"),
    Column("nalet_noch", Integer, nullable=False, doc="Налет  ВС  ночью"),
    Column("nalet_npmu", DateTime, nullable=False, doc="Налет  экипажей  в  НПМУ"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column("polet", Integer, nullable=False, doc="Количество  полетов  ВС"),
    Column("polet_den", Integer, nullable=False, doc="Количество  полетов  ВС  днем"),
    Column("polet_noch", Integer, nullable=False, doc="Количество  полетов  ВС  ночью"),
    Column(
        "procent_prognoz",
        Integer,
        nullable=False,
        doc="Количество  оправдавшихся  метеопрогнозов	целое",
    ),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    comment="Таблица  базы  данных  «Итоги  летной  деятельности,  за  периоды  времени  по  всем  типам  ВС»",
)

t_poteri_table = Table(
    "t_poteri",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("massiv", Integer[13][11], nullable=False, doc="Дата  начала  летной  смены"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    comment="Таблица  базы  данных  «Потери  в  результате  авиационных  событий,  за  периоды  времени»",
)

t_poteri_vs_table = Table(
    "t_poteri_vs",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("kod_vs", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column("poter", Integer, nullable=False, doc="Потеряно"),
    Column("pov", Integer, nullable=False, doc="Повреждено"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    Column("ser_pov", Integer, nullable=False, doc="Серьезно  повреждено"),
    comment="Таблица  базы  данных  «Потери  ВС  по  типам  по  периодам  времени»",
)

t_bezopasnost_table = Table(
    "t_bezopasnost",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("massiv", Integer[6][12], nullable=False, doc="данные"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    comment="Таблица  базы  данных  «Показатели  безопасности  полетов  за  период  времени»",
)

t_uroven_ls_table = Table(
    "t_uroven_ls",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("kod_vs", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("massiv", Integer[13], nullable=False, doc="данные"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    comment="Таблица  базы  данных  «Квалификация  и  уровень  подготовки  летного  состава  (летчики)»",
)

t_ispravnost_vs_table = Table(
    "t_ispravnost_vs",
    metadata,
    Column("arz", Integer, nullable=False, doc="Количество  на  АРЗ"),
    Column(
        "data", DateTime, nullable=False, doc="По  состоянию  на  <дата>  целое	(или  понедельник?)"
    ),
    Column("gotov", Integer, nullable=False, doc="Количество  готовых  к  полетам"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("ispr", Integer, nullable=False, doc="Количество  исправных"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("kod_vs", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("reglam", Integer, nullable=False, doc="Количество  на  регламентном  обслуживании"),
    Column("shtat", Integer, nullable=False, doc="Количество  по  штату"),
    Column(
        "t_vs_chasti_id",
        Integer,
        ForeignKey("t_vs_chasti.id"),
        nullable=False,
        doc="Количество  по  списку	целое	Из  таблицы  «Воздушные  суда  части»в  н",
    ),
    comment="Таблица  базы  данных  «Состояние  исправности  ВС»",
)

t_uchet_posled_table = Table(
    "t_uchet_posled",
    metadata,
    Column("data", DateTime, nullable=False, doc="Дата  события"),
    Column(
        "dop_identif",
        Integer,
        nullable=False,
        doc="Дополнительный  идентификатор  события  (автоматически  заполняется  «1»,  при  наличии  второго  и  последующих  событий  в  части  на  эту  же  дату    -    «+1»)	целое	Для  случая,  если  имело  место  более  одного  события  в  одной  летной  смене  (или  в  один  день)",
    ),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "k_podgr_id",
        Integer,
        ForeignKey("k_podgr.id"),
        nullable=False,
        doc="Код  подгруппы  причин",
    ),
    Column(
        "k_prichiny_id",
        Integer,
        ForeignKey("k_prichiny.id", name="fr_t_uchet_posled_k_prichiny_id"),
        nullable=False,
        doc="Код  пункта  в  подгруппе",
    ),
    Column("kod_prich", Integer, nullable=False, doc="Код  главной  причины"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("pog_ekipazh", Integer, nullable=False, doc="Погибло  членов  экипажа"),
    Column("pog_pass", Integer, nullable=False, doc="Погибло  пассажиров"),
    Column("pog_zem", Integer, nullable=False, doc="Погибло  на  земле"),
    Column("pos_ekipazh", Integer, nullable=False, doc="Пострадало  членов  экипажа"),
    Column("pos_pass", Integer, nullable=False, doc="Пострадало  пассажиров"),
    Column("pos_zem", Integer, nullable=False, doc="Пострадало  на  земле"),
    Column("poter", Integer, nullable=False, doc="Потеряно  ВС"),
    Column("pov", Integer, nullable=False, doc="Повреждено  ВС"),
    Column("ser_pov", Integer, nullable=False, doc="Серьезно  повреждено  ВС"),
    Column("ushcherb", Integer, nullable=False, doc="Материальный  ущерб  (руб.)"),
    comment="Таблица  базы  данных  «Оперативный  учет  авиационных  событий  и  их  последствий»",
)

t_uchet_poter_vs_table = Table(
    "t_uchet_poter_vs",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("kod_vs", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("poter", Integer, nullable=False, doc="Потеряно  ВС"),
    Column("pov", Integer, nullable=False, doc="Повреждено  ВС"),
    Column("ser_pov", Integer, nullable=False, doc="Серьезно  повреждено  ВС"),
    Column(
        "t_uchet_posled_id",
        Integer,
        ForeignKey("t_uchet_posled.id"),
        nullable=False,
        doc="ИД  записи  в  таблице  «Оперативный  учет  авиационных  событий  и  их  последствий»",
    ),
    comment="Таблица  базы  данных  данных  «Оперативный  учет  потерь  и  повреждений  ВС  по  типам»",
)

t_nedostatki_table = Table(
    "t_nedostatki",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("massiv", Integer[24][3], nullable=False, doc="данные"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета",
    ),
    comment="Таблица  базы  данных  данных  «Количество  нарушений  и  недостатков  по  периодам  времени»",
)

s_itog_vs_tip_table = Table(
    "s_itog_vs_tip",
    metadata,
    Column("god", DateTime, nullable=False, doc="Год  учета"),
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column(
        "kod_strukt",
        Integer,
        nullable=False,
        doc="Код  элемента  организационной  структуры  (части)",
    ),
    Column("kod_vs", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("nalet", DateTime, nullable=False, doc="Налет  ВС"),
    Column("nalet_den", Integer, nullable=False, doc="Налет  ВС  днем"),
    Column("nalet_dpmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДПМУ"),
    Column("nalet_dsmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДСМУ"),
    Column("nalet_ncmu", DateTime, nullable=False, doc="Налет  экипажей  в  НСМУ"),
    Column("nalet_noch", Integer, nullable=False, doc="Налет ВС ночью"),
    Column("nalet_npmu", DateTime, nullable=False, doc="Налет  экипажей  в  НПМУ"),
    Column("period", String(255), nullable=False, doc="Наименование  периода	текст"),
    Column("polet", Integer, nullable=False, doc="Количество  полетов  ВС"),
    Column("polet_den", Integer, nullable=False, doc="Количество  полетов  ВС  днем"),
    Column("polet_noch", Integer, nullable=False, doc="Количество  полетов  ВС  ночью"),
    Column(
        "s_period_ucheta_id",
        Integer,
        ForeignKey("s_period_ucheta.id"),
        nullable=False,
        doc="Код  периода  учета  целое",
    ),
    comment="Таблица  базы  данных  данных  «Итоги  летной  деятельности,  за  периоды  времени  по  типам  ВС»",
)

t_nalet_vs_table = Table(
    "t_nalet_vs",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, doc="id"),
    Column("kod_vs", Integer, nullable=False, doc="Код  типа  ВС"),
    Column("nalet", DateTime, nullable=False, doc="Налет  ВС"),
    Column("nalet_den", Integer, nullable=False, doc="Налет  ВС  днем"),
    Column("nalet_dpmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДПМУ"),
    Column("nalet_dsmu", DateTime, nullable=False, doc="Налет  экипажей  в  ДСМУ"),
    Column("nalet_ncmu", DateTime, nullable=False, doc="Налет  экипажей  в  НСМУ"),
    Column("nalet_noch", Integer, nullable=False, doc="Налет  ВС  ночью"),
    Column("nalet_npmu", DateTime, nullable=False, doc="Налет  экипажей  в  НПМУ"),
    Column("polet", Integer, nullable=False, doc="Количество  полетов  ВС"),
    Column("polet_den", Integer, nullable=False, doc="Количество  полетов  ВС  днем"),
    Column("polet_noch", Integer, nullable=False, doc="Количество  полетов  ВС  ночью"),
    Column(
        "t_plan_letnyh_smen_id",
        Integer,
        ForeignKey("t_plan_letnyh_smen.id"),
        nullable=False,
        doc="Планирование  и  выполнение  летных  смен",
    ),
    comment="Таблица  базы  данных  данных  «Учет  налета  ВС  и  экипаже  по  типам  ВС»",
)
