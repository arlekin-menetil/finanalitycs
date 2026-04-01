export default {
  auth: {
    login: "Kirish",
    phone: "Telefon",
    password: "Parol",
    submit: "Tizimga kirish",
  },

  profile: {
    title: "Moliyaviy profil",
    subtitle: "Shaxsiy tavsiyalar olish uchun ma'lumotlarni to‘ldiring",
    income: "Oylik daromad",
    expenses: "Oylik xarajatlar",
    creditScore: "Kredit reytingi",
    submit: "Profilni saqlash",
    loading: "Profil saqlanmoqda...",
    success: "Profil muvaffaqiyatli saqlandi",
  },

  dashboard: {
    title: "Boshqaruv paneli",
    score: "Kredit reytingi",
    approval: "Tasdiqlanish ehtimoli",
    risk: "Xavf darajasi",

    income: "Daromad",
    obligations: "Majburiyatlar",
    available: "Mavjud qoldiq",
    incomeVsObligations: "Daromad va majburiyatlar",

    debtLoad: "Qarz yuklamasi (DTI)",
    trend: "Tasdiqlanish dinamikasi",

    loading: "Moliyaviy profil yuklanmoqda...",
    error: "Skoring ma'lumotlarini yuklashda xatolik",

    riskLevels: {
      LOW: "Past xavf",
      MEDIUM: "O‘rtacha xavf",
      HIGH: "Yuqori xavf",
    },

    recommendations: "Bank tavsiyalari",

    topBanks: "Eng yaxshi bank takliflari",
    rate: "Foiz stavkasi",
    match: "Moslik",
    apply: "Ariza yuborish",
    bestMatch: "Eng yaxshi taklif",
    loadingRecommendations: "Tavsiyalar yuklanmoqda...",
    noRecommendations: "Mos takliflar topilmadi"
  },

  recommendations: {
    title: "Tavsiya etilgan banklar",
    subtitle: "Moliyaviy profilingiz asosida eng yaxshi kredit takliflari",

    loading: "Tavsiyalar yuklanmoqda...",
    empty: "Mos takliflar topilmadi",

    match: "Moslik",
    interest: "Foiz",
    approval: "Tasdiqlanish",
    loanLimit: "Kredit limiti",

    applyOnline: "Ariza yuborish",
    branches: "Filiallar",

    showMore: "Ko‘proq banklarni ko‘rsatish",
    bestOffer: "Eng yaxshi taklif",

    sortMatch: "Eng yaxshi moslik",
    sortRate: "Eng past foiz",
    sortApproval: "Eng yuqori tasdiqlanish",
    sortLimit: "Eng katta limit",

    filterAll: "Barchasi",
    filterMortgage: "Ipoteka",
    filterAuto: "Avtokredit",
    filterConsumer: "Iste'mol krediti"
  },

  scoring: {
    title: "Skoring ko‘rinishi",
    subtitle: "AI kredit xavf tahlili",
    recalc: "Qayta hisoblash",
    processing: "Hisoblanmoqda...",

    creditScore: "Kredit reytingi",
    riskLevel: "Xavf darajasi",
    approval: "Tasdiqlanish",
    model: "Model versiyasi",

    trend: "Natija dinamikasi",
    history: "Skoring tarixi",

    date: "Sana",
    time: "Vaqt",
    score: "Ball",

    toastSuccess: "Skoring muvaffaqiyatli yangilandi",
    toastError: "Hisoblashda xatolik"
  },

  branches: {
    title: "Bank filiallari",
    branch: "Filial",
    branches: "Filiallar",
    address: "Manzil",
    workingHours: "Ish vaqti",
    phone: "Telefon",
    city: "Shahar",
    showOnMap: "Xaritada ko‘rsatish"
  },

  analytics: {
    title: "Bank bozori analitikasi",
    loading: "Analitika yuklanmoqda...",

    totalBanks: "Banklar soni",
    averageInterest: "O‘rtacha foiz",
    averageApproval: "O‘rtacha tasdiqlanish ehtimoli",
    bestBank: "Eng yaxshi bank",

    interestRates: "Foiz stavkalari",
    approvalProbability: "Tasdiqlanish ehtimoli",
    loanLimits: "Kredit limitlari",
    rankingScores: "Reyting ballari",

    mobileDownloads: "Mobil ilova yuklab olishlar",
    mobileRatings: "Mobil ilova reytinglari",

    high: "Yuqori",
    medium: "O‘rtacha",
    low: "Past",

    marketMonitoring: "Bozor monitoringi",
    digitalRanking: "Banklarning raqamli reytingi",
    interestMonitor: "Foiz stavkalari monitoringi",
    marketForecast: "AI bozor prognozi",

    current: "Hozirgi",
    forecast30: "30 kun",
    forecast90: "90 kun"
  },

  alerts: {
    interest_drop: "foiz stavkasini {value}% ga kamaytirdi",
    installs_growth: "mobil ilova yuklab olishlar oshdi",
    rating_growth: "reyting {value} ga ko‘tarildi",

    rate_drop: "foiz stavkasini kamaytirdi",
    growth: "mobil ilova yuklab olishlar oshdi",
    rating: "reyting oshdi",

    rate_increase: "foiz stavkasini oshirdi",
    new_product: "yangi kredit mahsulotini ishga tushirdi",
    market_signal: "bozor signali aniqlangan"
  },

  products: {
    Mortgage: "Ipoteka",
    AutoLoan: "Avtokredit",
    ConsumerLoan: "Iste'mol krediti"
  },

  /* ---------------- 🔥 LANDING ---------------- */

  hero: {
    title: "Bank tahlili yangi darajada",
    subtitle: "Bank mahsulotlarini taqqoslang va AI yordamida eng yaxshisini toping"
  },

  common: {
    login: "Kirish"
  },

  stats: {
    banks: "Banklar",
    products: "Mahsulotlar",
    speed: "Bir necha soniya ichida AI tahlili"
  },

  data: {
    title: "Ma'lumot manbalari",
    desc: "Platforma ishonchli ma'lumot manbalaridan foydalanadi. Ma'lumotlar har 15 kunda yangilanadi.",
    bank: "Bank mahsulotlari, stavkalar va takliflar",
    deposit: "Depozitlar va foiz stavkalari",
    analytics: "Banklar bo‘yicha moliyaviy tahlil",
    gov: "Davlat va foydalanuvchi ma'lumotlari",
    credit: "Kredit tarixi va baholash"
  },

  benefits: {
    title: "Siz nimani olasiz",
    analytics: "Tahlil",
    analyticsDesc: "Bank mahsulotlarini chuqur tahlil qilish",
    ai: "AI",
    aiDesc: "Eng yaxshi takliflarni tanlash",
    speed: "Tezlik",
    speedDesc: "Natijalar soniyalar ichida",
    security: "Xavfsizlik",
    securityDesc: "Ma'lumotlaringiz himoyalangan"
  },

  chart: {
    title: "Valyuta kursi",
    mon: "Du",
    tue: "Se",
    wed: "Cho",
    thu: "Pa",
    fri: "Ju",
    sat: "Sha",
    sun: "Ya"
  },

  converter: {
    title: "Valyuta konvertori"
  }
}