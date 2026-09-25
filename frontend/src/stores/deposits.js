import { defineStore } from "pinia"
import api from "@/api/axios"

export const useDepositsStore = defineStore(
    "deposits",
    {
        state: () => ({

            // ==========================================
            // DATA
            // ==========================================
            items: [],

            // ==========================================
            // UI
            // ==========================================
            loading: false,

            error: null,

            // ==========================================
            // FILTERS
            // ==========================================
            filters: {

                search: "",

                bank: null,

                currency: "all",

                term: "all",

                online: false,

                rate: "all",
            },

            // ==========================================
            // SORT
            // ==========================================
            sort: "rate",
        }),

        // ==========================================
        // GETTERS
        // ==========================================
        getters: {

            // ==========================================
            // TOTAL COUNT
            // ==========================================
            totalCount: (state) => {

                return state.items.length
            },

            // ==========================================
            // 🏦 BANKS
            // ==========================================
            banks: (state) => {

                const grouped = {}

                state.items.forEach((item) => {

                    const bankName =
                        item.bank_name ||
                        item.bank ||
                        "Unknown Bank"

                    if (
                        bankName ===
                        "Unknown Bank"
                    ) {
                        return
                    }

                    grouped[bankName] =
                        (grouped[bankName] || 0) + 1
                })

                return Object
                    .entries(grouped)

                    .map(
                        ([name, count]) => ({
                            name,
                            count,
                        })
                    )

                    .sort((a, b) => {

                        return (
                            b.count -
                            a.count
                        )
                    })
            },
            // ==========================================
            // 🤖 RECOMMENDED BANKS
            // ==========================================

            recommendedBanks: (state) => {

                const grouped = {}

                // ======================================
                // ОБЯЗАТЕЛЬНЫЕ БАНКИ
                // ======================================

                const preferredBanks = [
                    "Hamkorbank",
                    "Aloqabank",
                ]

                // ======================================
                // GROUP DEPOSITS BY BANK
                // ======================================

                state.items.forEach((item) => {

                    const bankName =
                        item.bank_name ||
                        item.bank ||
                        "Unknown Bank"

                    if (
                        bankName ===
                        "Unknown Bank"
                    ) {
                        return
                    }

                    if (!grouped[bankName]) {

                        grouped[bankName] = {

                            name:
                                bankName,

                            count: 0,

                            totalRate: 0,

                            rates: [],

                            onlineCount: 0,

                            terms: [],

                            currencies: new Set(),

                            products: [],
                        }
                    }

                    const bank =
                        grouped[bankName]

                    const rate =
                        Number(
                            item.interest_rate ||
                            0
                        )

                    const term =
                        Number(
                            item.term ||
                            0
                        )

                    const isOnline =
                        Boolean(
                            item.is_online ||
                            item.real_online ||
                            item.online
                        )

                    const currency =
                        String(
                            item.currency ||
                            ""
                        )
                            .toUpperCase()
                            .trim()

                    bank.count++

                    if (rate > 0) {

                        bank.totalRate += rate

                        bank.rates.push(
                            rate
                        )
                    }

                    if (term > 0) {

                        bank.terms.push(
                            term
                        )
                    }

                    if (isOnline) {

                        bank.onlineCount++
                    }

                    if (currency) {

                        bank.currencies.add(
                            currency
                        )
                    }

                    bank.products.push(
                        item
                    )
                })

                // ======================================
                // FIND MAX VALUES
                // ======================================

                const bankValues =
                    Object.values(grouped)

                if (!bankValues.length) {

                    return []
                }

                const maxRate =
                    Math.max(
                        ...bankValues.flatMap(
                            bank =>
                                bank.rates
                        ),
                        1
                    )

                const maxProducts =
                    Math.max(
                        ...bankValues.map(
                            bank =>
                                bank.count
                        ),
                        1
                    )

                // ======================================
                // CALCULATE SCORE
                // ======================================

                const result =
                    bankValues.map(
                        (bank) => {

                            const averageRate =
                                bank.rates.length
                                    ? bank.totalRate /
                                    bank.rates.length
                                    : 0

                            const bestRate =
                                bank.rates.length
                                    ? Math.max(
                                        ...bank.rates
                                    )
                                    : 0

                            // Ставка
                            const rateScore =
                                (
                                    bestRate /
                                    maxRate
                                ) * 55

                            // Онлайн
                            const onlineRatio =
                                bank.count > 0
                                    ? bank.onlineCount /
                                    bank.count
                                    : 0

                            const onlineScore =
                                onlineRatio * 15

                            // Количество продуктов
                            const productScore =
                                (
                                    bank.count /
                                    maxProducts
                                ) * 10

                            // Средний срок
                            const averageTerm =
                                bank.terms.length
                                    ? bank.terms.reduce(
                                        (sum, value) =>
                                            sum + value,
                                        0
                                    ) /
                                    bank.terms.length
                                    : 0

                            const termScore =
                                Math.min(
                                    averageTerm / 36,
                                    1
                                ) * 10

                            // Валюты
                            const currencyScore =
                                Math.min(
                                    bank.currencies.size / 3,
                                    1
                                ) * 10

                            const score =
                                Math.round(
                                    Math.min(
                                        rateScore +
                                        onlineScore +
                                        productScore +
                                        termScore +
                                        currencyScore,
                                        100
                                    )
                                )

                            return {

                                name:
                                    bank.name,

                                count:
                                    bank.count,

                                score,

                                match_score:
                                    score,

                                average_rate:
                                    Math.round(
                                        averageRate * 100
                                    ) / 100,

                                best_rate:
                                    bestRate,

                                online_count:
                                    bank.onlineCount,

                                online_ratio:
                                    Math.round(
                                        onlineRatio * 100
                                    ),

                                average_term:
                                    Math.round(
                                        averageTerm * 100
                                    ) / 100,

                                currencies:
                                    Array.from(
                                        bank.currencies
                                    ),

                                products:
                                    bank.products,
                            }
                        }
                    )

                // ======================================
                // ОБЯЗАТЕЛЬНЫЕ БАНКИ
                // ======================================

                const preferred =
                    result
                        .filter(
                            bank =>
                                preferredBanks.includes(
                                    bank.name
                                )
                        )
                        .sort((a, b) => {

                            return (
                                preferredBanks.indexOf(
                                    a.name
                                ) -
                                preferredBanks.indexOf(
                                    b.name
                                )
                            )
                        })

                // ======================================
                // ОСТАЛЬНЫЕ БАНКИ
                // ======================================

                const others =
                    result
                        .filter(
                            bank =>
                                !preferredBanks.includes(
                                    bank.name
                                )
                        )
                        .sort((a, b) => {

                            if (
                                b.score !==
                                a.score
                            ) {

                                return (
                                    b.score -
                                    a.score
                                )
                            }

                            if (
                                b.best_rate !==
                                a.best_rate
                            ) {

                                return (
                                    b.best_rate -
                                    a.best_rate
                                )
                            }

                            return (
                                b.count -
                                a.count
                            )
                        })

                // ======================================
                // FINAL RECOMMENDATIONS
                // ======================================
                // Hamkorbank + Aloqabank
                // + ещё 4 банка по реальному score
                // ======================================

                return [
                    ...preferred,
                    ...others,
                ].slice(0, 6)
            },
            // ==========================================
            // 💰 FILTERED DEPOSITS
            // ==========================================
            filteredDeposits: (state) => {

                let data = [
                    ...state.items
                ]

                // ======================================
                // SEARCH
                // ======================================
                if (
                    state.filters.search
                ) {

                    const query =
                        String(
                            state.filters.search
                        )
                            .toLowerCase()
                            .trim()

                    data = data.filter(
                        (item) => {

                            const productName =
                                String(
                                    item.product_name ||
                                    item.name ||
                                    ""
                                )
                                    .toLowerCase()

                            const bankName =
                                String(
                                    item.bank_name ||
                                    ""
                                )
                                    .toLowerCase()

                            return (
                                productName.includes(
                                    query
                                ) ||
                                bankName.includes(
                                    query
                                )
                            )
                        }
                    )
                }

                // ======================================
                // BANK
                // ======================================
                if (
                    state.filters.bank
                ) {

                    data = data.filter(
                        (item) =>
                            item.bank_name ===
                            state.filters.bank
                    )
                }

                // ======================================
                // CURRENCY
                // ======================================
                if (
                    state.filters.currency !==
                    "all"
                ) {

                    data = data.filter(
                        (item) => {

                            const currency =
                                String(
                                    item.currency ||
                                    ""
                                )
                                    .toUpperCase()
                                    .trim()

                            return (
                                currency ===
                                state.filters.currency
                                    .toUpperCase()
                            )
                        }
                    )
                }

                // ======================================
                // ONLINE
                // ======================================
                if (
                    state.filters.online
                ) {

                    data = data.filter(
                        (item) => {

                            return Boolean(
                                item.is_online ||
                                item.real_online ||
                                item.online
                            )
                        }
                    )
                }

                // ======================================
                // HIGH RATE
                // ======================================
                if (
                    state.filters.rate ===
                    "high"
                ) {

                    data = data.filter(
                        (item) =>
                            Number(
                                item.interest_rate ||
                                0
                            ) >= 20
                    )
                }

                // ======================================
                // SORT
                // ======================================
                switch (
                state.sort
                ) {

                    case "rate":

                        data.sort(
                            (a, b) =>
                                Number(
                                    b.interest_rate ||
                                    0
                                ) -
                                Number(
                                    a.interest_rate ||
                                    0
                                )
                        )

                        break

                    case "term":

                        data.sort(
                            (a, b) =>
                                Number(
                                    b.term ||
                                    0
                                ) -
                                Number(
                                    a.term ||
                                    0
                                )
                        )

                        break

                    case "bank":

                        data.sort(
                            (a, b) =>
                                String(
                                    a.bank_name ||
                                    ""
                                ).localeCompare(
                                    String(
                                        b.bank_name ||
                                        ""
                                    )
                                )
                        )

                        break
                }

                return data
            },

            // ==========================================
            // 📈 AVERAGE RATE
            // ==========================================
            averageRate: (state) => {

                const rates =
                    state.items
                        .map(
                            (item) =>
                                Number(
                                    item.interest_rate
                                )
                        )
                        .filter(
                            (value) =>
                                !isNaN(value)
                        )

                if (
                    !rates.length
                ) {
                    return 0
                }

                return Math.round(
                    rates.reduce(
                        (sum, value) =>
                            sum + value,
                        0
                    ) /
                    rates.length
                )
            },
        },

        // ==========================================
        // ACTIONS
        // ==========================================
        actions: {

            // ==========================================
            // LOAD
            // ==========================================

            async load() {

                try {

                    this.loading = true

                    this.error = null

                    const response =
                        await api.get(
                            "/banks/products/",
                            {
                                params: {
                                    type: "deposit",
                                    limit: 500,
                                },
                            }
                        )

                    const data =
                        response?.data

                    let list = []

                    if (
                        Array.isArray(data)
                    ) {

                        list = data

                    } else {

                        list =
                            data?.results ||
                            data?.products ||
                            []
                    }

                    // ======================================
                    // NORMALIZE
                    // ======================================

                    this.items =
                        list.map(
                            (item) => {

                                const rate =
                                    Number(
                                        item.interest_rate ||
                                        0
                                    )

                                return {

                                    ...item,

                                    product_name:
                                        item.product_name ||
                                        item.name ||
                                        "Вклад",

                                    bank_name:
                                        item.bank_name ||
                                        item.bank?.name ||
                                        "Unknown Bank",

                                    interest_rate:
                                        rate || null,

                                    term:
                                        item.term ||
                                        null,

                                    is_online:
                                        Boolean(
                                            item.is_online ||
                                            item.real_online ||
                                            item.online
                                        ),

                                    website:
                                        item.website ||
                                        item.source_url ||
                                        item.bank_url ||
                                        null,
                                }
                            }
                        )

                    console.log(
                        "DEPOSITS:",
                        this.items.length
                    )

                    console.log(
                        "BANKS:",
                        this.banks
                    )

                    console.log(
                        "RECOMMENDED:",
                        this.recommendedBanks
                    )

                } catch (error) {

                    console.error(
                        "Deposits load failed",
                        error
                    )

                    this.error =
                        error?.response?.data ||
                        error?.message ||
                        "Failed to load deposits"

                    this.items = []

                } finally {

                    this.loading = false
                }
            },

            // ==========================================
            // RESET
            // ==========================================

            reset() {

                this.items = []

                this.loading = false

                this.error = null

                this.filters = {

                    search: "",

                    bank: null,

                    currency: "all",

                    term: "all",

                    online: false,

                    rate: "all",
                }

                this.sort = "rate"
            },
        },
    }
)