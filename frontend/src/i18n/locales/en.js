export default {
  // =========================================================
  // AUTH — Авторизация
  // =========================================================

  auth: {
    login: "Login",
    phone: "Phone",
    password: "Password",
    submit: "Sign In",
  },

  // =========================================================
  // PROFILE — Финансовый профиль
  // =========================================================

  profile: {
    title: "Financial Profile",

    subtitle:
      "Fill in your financial data to get personalized recommendations",

    income: "Monthly Income",
    expenses: "Monthly Expenses",
    creditScore: "Credit Score",

    submit: "Save Profile",
    loading: "Saving profile...",
    success: "Profile successfully saved",
  },

  // =========================================================
  // DASHBOARD — Панель управления
  // =========================================================

  dashboard: {
    title: "Dashboard",

    welcome: "Welcome",

    financialCabinet: "Your financial cabinet",

    description:
      "Creditworthiness analysis based on your official credit history and BankAnalytics AI model.",

    score: "Credit Score",
    approval: "Approval Probability",
    risk: "Risk Category",

    income: "Income",
    obligations: "Obligations",
    expenses: "Expenses",
    available: "Available",

    freeBalance: "Free Balance",

    incomeVsObligations: "Income vs Obligations",

    debtLoad: "Debt Load (DTI)",
    trend: "Approval Trend",

    loading: "Loading financial profile...",
    error: "Failed to load scoring data",

    // ---------------------------------------------------------
    // Risk
    // ---------------------------------------------------------

    riskLevels: {
      LOW: "Low Risk",
      MEDIUM: "Medium Risk",
      HIGH: "High Risk",
      REJECT: "High Credit Risk",
      UNKNOWN: "Insufficient Data",

      low: "Low Risk",
      medium: "Medium Risk",
      high: "High Risk",
      reject: "High Credit Risk",
      unknown: "Insufficient Data",
    },

    // ---------------------------------------------------------
    // Credit analysis
    // ---------------------------------------------------------

    creditAnalysis: "Credit Analysis",

    financialScoring: "Client Financial Scoring",

    officialCreditScore: "Official Credit Score",

    aiCreditScore: "AI Credit Score",

    creditBureau: "Credit Bureau",

    aiScore: "AI Score",

    creditworthiness: "Creditworthiness",

    scoreCalculated:
      "AI score is calculated based on your financial profile.",

    scoreRange: "Score Range",

    // ---------------------------------------------------------
    // Approval
    // ---------------------------------------------------------

    approvalSection: "Approval",

    approvalProbability: "Approval Probability",

    estimatedProbability: "Estimated Probability",

    highProbability: "High Probability",

    mediumProbability: "Medium Probability",

    lowProbability: "Low Probability",

    // ---------------------------------------------------------
    // Credit limit
    // ---------------------------------------------------------

    recommendedLimit: "Recommended Credit Limit",

    limitDescription:
      "Estimated guideline based on your current financial profile.",

    // ---------------------------------------------------------
    // Financial snapshot
    // ---------------------------------------------------------

    financialSnapshot: "Financial Snapshot",

    financialInformation: "Financial Information",

    totalDebt: "Total Debt",

    contracts: "Contracts",

    contractCount: "Number of Contracts",

    dti: "Debt-to-Income Ratio",

    netBalance: "Free Balance",

    // ---------------------------------------------------------
    // AI analysis
    // ---------------------------------------------------------

    aiAnalysis: "AI Analysis",

    aiMetrics: "AI Model Metrics",

    history: "Credit History",

    profileScore: "Profile Score",

    employmentScore: "Employment Score",

    // ---------------------------------------------------------
    // Dashboard recommendations
    // Это рекомендации именно внутри Dashboard
    // ---------------------------------------------------------

    recommendations: "Bank Recommendations",

    topBanks: "Top Bank Matches",

    recommendationsTitle: "AI Recommendations",

    recommendationsDescription:
      "Best banking products selected based on your financial profile and AI scoring.",

    recommendationsCount: "recommendations",

    rate: "Interest Rate",

    match: "Match",

    apply: "Apply",

    bestMatch: "Best Match",

    loadingRecommendations: "Loading recommendations...",

    noRecommendations: "No recommendations available",

    showMore: "Show More",

    // ---------------------------------------------------------
    // Profile / analysis status
    // ---------------------------------------------------------

    lastAiAnalysis: "Last AI Analysis",

    profileVersion: "Profile Version",

    analysisCompleted: "Analysis Completed",

    profile: "Profile",

    profileCompleted: "Profile Completed",

    profileNotCompleted: "Profile Not Completed",

    employment: "Employment",

    employmentVerified: "Employment Verified",

    employmentNotVerified: "Employment Not Verified",

    // ---------------------------------------------------------
    // AI metrics
    // ---------------------------------------------------------

    metrics: {
      income: "Income",
      dti: "Debt-to-Income",
      employment: "Employment",
      history: "Credit History",
      profile: "Profile",
      netBalance: "Net Balance",
    },
  },

  // =========================================================
  // RECOMMENDATIONS — Страница рекомендаций
  // =========================================================

  recommendations: {
    // ---------------------------------------------------------
    // Page header
    // ---------------------------------------------------------

    title: "Recommended Banks",

    subtitle:
      "Best loan offers based on your financial profile",

    loading: "Loading recommendations...",

    empty: "No recommendations available",

    // ---------------------------------------------------------
    // Hero
    // ---------------------------------------------------------

    hero: {
      badge: "AI-powered recommendations",

      title: "Personalized recommendations",

      description:
        "Find the most suitable banking products based on your financial profile and AI scoring.",
    },

    // ---------------------------------------------------------
    // Statistics
    // ---------------------------------------------------------

    stats: {
      products: "products",
      banks: "banks",
    },

    // ---------------------------------------------------------
    // Sections
    // ---------------------------------------------------------

    sections: {
      recommendedBanks: "Recommended banks",
      allProducts: "All products",
    },

    // ---------------------------------------------------------
    // AI
    // ---------------------------------------------------------

    aiRating: "AI Rating",

    // ---------------------------------------------------------
    // Recommendation metrics
    // ---------------------------------------------------------

    match: "Match",

    interest: "Interest Rate",

    approval: "Approval",

    loanLimit: "Loan Limit",

    applyOnline: "Apply Online",

    branches: "Branches",

    showMore: "Show More Banks",

    bestOffer: "Best Offer",

    // ---------------------------------------------------------
    // Sorting
    // ---------------------------------------------------------

    sortMatch: "Best Match",

    sortRate: "Lowest Interest Rate",

    sortApproval: "Highest Approval Probability",

    sortLimit: "Highest Limit",

    // ---------------------------------------------------------
    // Product filters
    // ---------------------------------------------------------

    filterAll: "All",

    filterLoan: "Loans",

    filterMicro: "Microloans",

    filterMortgage: "Mortgage",

    filterAuto: "Auto Loans",

    filterEducation: "Education",

    filterGreen: "Green",

    filterOverdraft: "Overdraft",

    filterCard: "Cards",

    filterInstallment: "Installments",

    filterBusiness: "Business",

    filterConsumer: "Consumer Loans",

    // ---------------------------------------------------------
    // Product information
    // ---------------------------------------------------------

    product: "Product",

    bank: "Bank",

    term: "Term",

    type: "Loan Type",

    online: "Online",

    offline: "At Branch",

    onlineOnly: "Online Only",

    // ---------------------------------------------------------
    // Bank filter
    // ---------------------------------------------------------

    allBanks: "All Banks",

    // ---------------------------------------------------------
    // Counters
    // ---------------------------------------------------------

    offers: "offers",

    products: "products",
  },

  // =========================================================
  // SCORING — Скоринг
  // =========================================================

  scoring: {
    title: "Scoring Overview",

    subtitle:
      "Real-time AI credit analytics",

    recalc: "Recalculate Score",

    processing: "Processing...",

    creditScore: "Credit Score",

    riskLevel: "Risk Level",

    approval: "Approval",

    model: "Model Version",

    trend: "Performance Trend",

    history: "Scoring History",

    date: "Date",

    time: "Time",

    score: "Score",

    // ---------------------------------------------------------
    // Current score
    // ---------------------------------------------------------

    lastCalculation: "Last Calculation",

    currentScore: "Current AI Score",

    scoreDescription:
      "Financial profile analysis result",

    recommendedLimit: "Recommended Limit",

    limitDescription:
      "Calculated credit limit",

    aiScore: "AI Scoring",

    estimatedProbability:
      "Estimated Probability",

    currentRisk:
      "Current Risk Level",

    // ---------------------------------------------------------
    // Trend
    // ---------------------------------------------------------

    trendDescription:
      "Credit score movement across recent calculations",

    // ---------------------------------------------------------
    // Scoring factors
    // ---------------------------------------------------------

    aiBreakdown: "Scoring Factors",

    breakdownDescription:
      "Key indicators affecting the final score",

    income: "Income",

    dti: "Debt-to-Income",

    employment: "Employment",

    creditHistory: "Credit History",

    profile: "Financial Profile",

    // ---------------------------------------------------------
    // Statistics
    // ---------------------------------------------------------

    average: "Average",

    minimum: "Minimum",

    maximum: "Maximum",

    periodChange: "Period Change",

    change: "Change",

    // ---------------------------------------------------------
    // History
    // ---------------------------------------------------------

    historyDescription:
      "Latest 20 credit score calculations",

    noData: "No Scoring Data",

    noDataDescription:
      "Run a calculation to get your current credit score.",

    noHistory:
      "No scoring history yet",

    // ---------------------------------------------------------
    // Limits / errors
    // ---------------------------------------------------------

    dailyLimit:
      "Scoring can only be recalculated once per day",

    loadError:
      "Failed to load scoring data",

    // ---------------------------------------------------------
    // Notifications
    // ---------------------------------------------------------

    toastSuccess:
      "Score successfully recalculated",

    toastError:
      "Calculation failed",

    // ---------------------------------------------------------
    // Risk levels
    // ---------------------------------------------------------

    risk: {
      low: "Low",
      medium: "Medium",
      high: "High",
      reject: "Critical",
    },
  },

  // =========================================================
  // BRANCHES — Филиалы
  // =========================================================

  branches: {
    title: "Bank Branches",

    branch: "Branch",

    branches: "Branches",

    address: "Address",

    workingHours: "Working Hours",

    phone: "Phone",

    city: "City",

    showOnMap: "Show on Map",

    loading: "Loading branches...",

    empty: "No branches found",

    monday: "Monday",

    tuesday: "Tuesday",

    wednesday: "Wednesday",

    thursday: "Thursday",

    friday: "Friday",

    saturday: "Saturday",

    sunday: "Sunday",
  },

  // =========================================================
  // ANALYTICS — Аналитика
  // =========================================================

  analytics: {
    title: "Bank Market Analytics",

    loading: "Loading analytics...",

    totalBanks: "Total Banks",

    averageInterest: "Average Interest Rate",

    averageApproval: "Average Approval Probability",

    bestBank: "Best Offer",

    interestRates: "Market Interest Rates",

    approvalProbability: "Approval Probability",

    loanLimits: "Loan Limits",

    rankingScores: "Recommendation Scores",

    mobileDownloads: "Mobile App Downloads",

    mobileRatings: "Mobile App Ratings",

    high: "High",

    medium: "Medium",

    low: "Low",

    marketMonitoring: "Market Monitoring",

    digitalRanking: "Digital Bank Ranking",

    interestMonitor: "Interest Rate Monitor",

    marketForecast: "AI Market Forecast",

    current: "Current",

    forecast30: "30 Days",

    forecast90: "90 Days",

    bankComparison: "Bank Comparison",

    productComparison: "Product Comparison",

    marketAverage: "Market Average",
  },

  // =========================================================
  // ALERTS — Уведомления
  // =========================================================

  alerts: {
    interest_drop:
      "lowered interest rate by {value}%",

    installs_growth:
      "mobile installs increased",

    rating_growth:
      "rating increased to {value}",

    rate_drop:
      "lowered interest rate",

    growth:
      "mobile installs increased",

    rating:
      "rating increased",

    rate_increase:
      "increased interest rate by {value}%",

    new_product:
      "launched a new loan product",

    market_signal:
      "market signal detected",
  },

  // =========================================================
  // PRODUCTS — Типы продуктов
  // =========================================================

  products: {
    Mortgage: "Mortgage",

    AutoLoan: "Auto Loan",

    ConsumerLoan: "Consumer Loan",

    business_credit: "Business Loan",

    micro: "Microloan",

    consumer: "Consumer Loan",

    mortgage: "Mortgage",

    auto: "Auto Loan",

    credit: "Credit",

    loan: "Loan",
  },

  // =========================================================
  // LANDING — Главная страница
  // =========================================================

  hero: {
    title: "Bank Analysis on a New Level",

    subtitle:
      "Compare banking products and find the best offers using AI",

    getStarted: "Get Started",

    learnMore: "Learn More",
  },

  // =========================================================
  // COMMON — Общие элементы
  // =========================================================

  common: {
    login: "Login",

    logout: "Logout",

    save: "Save",

    cancel: "Cancel",

    close: "Close",

    confirm: "Confirm",

    yes: "Yes",

    no: "No",

    loading: "Loading...",

    error: "Error",

    success: "Success",

    search: "Search",

    filter: "Filter",

    reset: "Reset",

    refresh: "Refresh",

    next: "Next",

    back: "Back",

    previous: "Previous",

    details: "Details",

    viewAll: "View All",

    online: "Online",

    offline: "Offline",

    ai: "BankAnalytics AI",
  },

  // =========================================================
  // NAVIGATION — Навигация
  // =========================================================

  nav: {
    dashboard: "Dashboard",

    scoring: "Scoring",

    recommendations: "Recommendations",

    analytics: "Analytics",

    monitoring: "Monitoring",

    deposits: "Deposits",

    cards: "Cards",

    profile: "Profile",

    branches: "Branches",

    logout: "Logout",
  },

  // =========================================================
  // BRAND — Бренд
  // =========================================================

  brand: {
    name: "FinAnalytics",

    financial: "Financial",

    intelligence: "Intelligence",
  },

  // =========================================================
  // LANGUAGES — Языки
  // =========================================================

  languages: {
    ru: "Russian",

    en: "English",

    uz: "Uzbek",
  },

  // =========================================================
  // CURRENCY — Валюта
  // =========================================================

  currency: {
    uzs: "UZS",

    symbol: "UZS",
  },

  // =========================================================
  // STATS — Статистика
  // =========================================================

  stats: {
    banks: "Banks",

    products: "Products",

    speed: "AI Analysis in Seconds",
  },

  // =========================================================
  // DATA SOURCES — Источники данных
  // =========================================================

  data: {
    title: "Data Sources",

    desc:
      "The platform uses trusted data sources. Information is updated every 15 days.",

    bank:
      "Current banking products, rates and offers",

    deposit:
      "Deposit data and interest rates",

    analytics:
      "Financial indicators and bank analytics",

    gov:
      "Government and user data",

    credit:
      "Credit history and scoring data",
  },

  // =========================================================
  // BENEFITS — Преимущества
  // =========================================================

  benefits: {
    title: "Monitoring",

    analytics: "Analytics",

    analyticsDesc:
      "Deep analysis of banking products",

    ai: "AI",

    aiDesc:
      "Smart recommendations",

    speed: "Speed",

    speedDesc:
      "Results in seconds",

    security: "Security",

    securityDesc:
      "Your data is protected",
  },

  // =========================================================
  // CHART — Графики
  // =========================================================

  chart: {
    title: "Exchange Rate",

    mon: "Mon",

    tue: "Tue",

    wed: "Wed",

    thu: "Thu",

    fri: "Fri",

    sat: "Sat",

    sun: "Sun",
  },

  // =========================================================
  // CONVERTER — Конвертер валют
  // =========================================================

  converter: {
    title: "Currency Converter",

    from: "From",

    to: "To",

    amount: "Amount",

    result: "Result",

    swap: "Swap Currencies",
  },
}