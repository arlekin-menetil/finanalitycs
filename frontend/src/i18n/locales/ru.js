export default {
  auth: {
    login: "Вход",
    phone: "Телефон",
    password: "Пароль",
    submit: "Войти",
  },

  profile: {
    title: "Финансовый профиль",
    subtitle: "Заполните данные для получения персональных рекомендаций",
    income: "Ежемесячный доход",
    expenses: "Ежемесячные расходы",
    creditScore: "Кредитный рейтинг",
    submit: "Сохранить профиль",
    loading: "Сохранение профиля...",
    success: "Профиль успешно сохранён",
  },

  dashboard: {
    title: "Панель управления",
    score: "Кредитный рейтинг",
    approval: "Вероятность одобрения",
    risk: "Категория риска",

    income: "Доход",
    obligations: "Обязательства",
    available: "Доступно",
    incomeVsObligations: "Доход и обязательства",

    debtLoad: "Долговая нагрузка (DTI)",
    trend: "Динамика одобрения",

    loading: "Загрузка финансового профиля...",
    error: "Ошибка загрузки скоринга",

    riskLevels: {
      LOW: "Низкий риск",
      MEDIUM: "Средний риск",
      HIGH: "Высокий риск",
    },

    recommendations: "Рекомендации банков",

    topBanks: "Лучшие предложения банков",
    rate: "Ставка",
    match: "Совпадение",
    apply: "Подать заявку",
    bestMatch: "Лучшее предложение",
    loadingRecommendations: "Загрузка рекомендаций...",
    noRecommendations: "Нет доступных предложений"
  },

  recommendations: {
    title: "Рекомендуемые банки",
    subtitle: "Лучшие кредитные предложения на основе вашего профиля",

    loading: "Загрузка рекомендаций...",
    empty: "Нет доступных предложений",

    match: "Совпадение",
    interest: "Ставка",
    approval: "Одобрение",
    loanLimit: "Лимит кредита",

    applyOnline: "Подать заявку",
    branches: "Филиалы",

    showMore: "Показать больше банков",
    bestOffer: "Лучшее предложение",

    sortMatch: "Лучшее совпадение",
    sortRate: "Минимальная ставка",
    sortApproval: "Максимальное одобрение",
    sortLimit: "Максимальный лимит",

    filterAll: "Все",
    filterMortgage: "Ипотека",
    filterAuto: "Автокредит",
    filterConsumer: "Потребительский кредит"
  },

  scoring: {
    title: "Обзор скоринга",
    subtitle: "AI-анализ кредитного риска",
    recalc: "Пересчитать скоринг",
    processing: "Обработка...",

    creditScore: "Кредитный рейтинг",
    riskLevel: "Уровень риска",
    approval: "Одобрение",
    model: "Версия модели",

    trend: "Динамика показателей",
    history: "История скоринга",

    date: "Дата",
    time: "Время",
    score: "Балл",

    toastSuccess: "Скоринг успешно пересчитан",
    toastError: "Ошибка пересчёта"
  },

  branches: {
    title: "Филиалы банка",
    branch: "Филиал",
    branches: "Филиалы",
    address: "Адрес",
    workingHours: "Часы работы",
    phone: "Телефон",
    city: "Город",
    showOnMap: "Показать на карте"
  },

  analytics: {
    title: "Аналитика банковского рынка",
    loading: "Загрузка аналитики...",

    totalBanks: "Количество банков",
    averageInterest: "Средняя ставка",
    averageApproval: "Средняя вероятность одобрения",
    bestBank: "Лучший банк",

    interestRates: "Процентные ставки",
    approvalProbability: "Вероятность одобрения",
    loanLimits: "Лимиты кредитов",
    rankingScores: "Рейтинг рекомендаций",

    mobileDownloads: "Скачивания мобильных приложений",
    mobileRatings: "Рейтинг мобильных приложений",

    high: "Высокая",
    medium: "Средняя",
    low: "Низкая",

    marketMonitoring: "Мониторинг рынка",
    digitalRanking: "Цифровой рейтинг банков",
    interestMonitor: "Мониторинг процентных ставок",
    marketForecast: "AI прогноз рынка",

    current: "Текущие",
    forecast30: "30 дней",
    forecast90: "90 дней"
  },

  alerts: {
    interest_drop: "снизил процентную ставку на {value}%",
    installs_growth: "рост установок мобильного приложения",
    rating_growth: "рейтинг вырос до {value}",

    rate_drop: "снизил процентную ставку",
    growth: "рост установок мобильного приложения",
    rating: "рейтинг вырос",

    rate_increase: "повысил процентную ставку",
    new_product: "запустил новый кредитный продукт",
    market_signal: "обнаружен рыночный сигнал"
  },

  products: {
    Mortgage: "Ипотека",
    AutoLoan: "Автокредит",
    ConsumerLoan: "Потребительский кредит"
  },

  /* ---------------- 🔥 НОВОЕ (LANDING) ---------------- */

  hero: {
    title: "Анализ банков на новом уровне",
    subtitle: "Сравнивайте банковские продукты и находите лучшие предложения с помощью AI"
  },

  common: {
    login: "Войти"
  },

  stats: {
    banks: "Банка",
    products: "Продуктов",
    speed: "AI анализ за секунды"
  },

  data: {
    title: "Источники данных",
    desc: "Платформа использует проверенные источники данных. Информация обновляется каждые 15 дней.",
    bank: "Актуальные банковские продукты, ставки и предложения",
    deposit: "Данные по депозитам и процентным ставкам",
    analytics: "Финансовые показатели и аналитика банков",
    gov: "Государственные данные и пользовательская информация",
    credit: "Кредитная история и оценка платежеспособности"
  },

  benefits: {
    title: "Что ты получаешь",
    analytics: "Аналитика",
    analyticsDesc: "Глубокий анализ банковских продуктов",
    ai: "AI",
    aiDesc: "Подбор лучших предложений",
    speed: "Скорость",
    speedDesc: "Результаты за секунды",
    security: "Безопасность",
    securityDesc: "Данные защищены"
  },

  chart: {
    title: "Курс валют",
    mon: "Пн",
    tue: "Вт",
    wed: "Ср",
    thu: "Чт",
    fri: "Пт",
    sat: "Сб",
    sun: "Вс"
  },

  converter: {
    title: "Конвертер валют"
  }
}