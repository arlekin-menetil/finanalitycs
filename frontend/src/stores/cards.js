import { defineStore } from "pinia"
import api from "@/api/axios"

export const useCardsStore = defineStore(
    "cards",
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

                system: "all",

                online: false,
            },

            // ==========================================
            // SORT
            // ==========================================
            sort: "bank",
        }),

        // ==========================================
        // GETTERS
        // ==========================================
        getters: {

            totalCount: (state) => {

                return state.items.length
            },

            // ==========================================
            // 🏦 BANKS
            // ==========================================
            banks: (state) => {

                const priorityBanks = [

                    "Hamkorbank",

                    "Aloqabank",

                    "Kapitalbank",

                    "SQB",

                    "NBU",

                    "Ipak Yuli Bank",

                    "Uzum Bank",

                ]

                const grouped = {}

                state.items.forEach((item) => {

                    const bankName =
                        item.bank_name ||
                        item.bank?.name ||
                        "Unknown Bank"

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

                        const aPriority =
                            priorityBanks.indexOf(
                                a.name
                            )

                        const bPriority =
                            priorityBanks.indexOf(
                                b.name
                            )

                        if (
                            aPriority !== -1 &&
                            bPriority !== -1
                        ) {

                            return (
                                aPriority -
                                bPriority
                            )
                        }

                        if (
                            aPriority !== -1
                        ) {
                            return -1
                        }

                        if (
                            bPriority !== -1
                        ) {
                            return 1
                        }

                        return (
                            b.count -
                            a.count
                        )
                    })
            },

            // ==========================================
            // 💳 FILTERED CARDS
            // ==========================================
            filteredCards: (state) => {

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
                                    item.name || ""
                                ).toLowerCase()

                            const bankName =
                                String(
                                    item.bank_name || ""
                                ).toLowerCase()

                            return (
                                productName.includes(query) ||
                                bankName.includes(query)
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
                    state.filters.currency !== "all"
                ) {

                    data = data.filter(
                        (item) => {

                            const currency =
                                String(
                                    item.currency || ""
                                ).toUpperCase()

                            return (
                                currency ===
                                state.filters.currency.toUpperCase()
                            )
                        }
                    )
                }

                // ======================================
                // CARD SYSTEM
                // ======================================
                if (
                    state.filters.system !== "all"
                ) {

                    data = data.filter(
                        (item) => {

                            const system =
                                String(
                                    item.raw_data?.card_system ||
                                    item.card_system ||
                                    ""
                                ).toUpperCase()

                            return (
                                system ===
                                state.filters.system.toUpperCase()
                            )
                        }
                    )
                }

                // ======================================
                // ONLINE
                // ======================================
                // ======================================
                // ONLINE
                // ======================================
                if (state.filters.online) {

                    data = data.filter(
                        (item) =>
                            Boolean(
                                item.is_online
                            )
                    )
                }

                // ======================================
                // SORT
                // ======================================
                switch (state.sort) {

                    case "currency":

                        data.sort(
                            (a, b) =>
                                String(
                                    a.currency || ""
                                ).localeCompare(
                                    String(
                                        b.currency || ""
                                    )
                                )
                        )

                        break

                    case "name":

                        data.sort(
                            (a, b) =>
                                String(
                                    a.name || ""
                                ).localeCompare(
                                    String(
                                        b.name || ""
                                    )
                                )
                        )

                        break

                    case "bank":

                    default:

                        data.sort(
                            (a, b) =>
                                String(
                                    a.bank_name || ""
                                ).localeCompare(
                                    String(
                                        b.bank_name || ""
                                    )
                                )
                        )

                        break
                }

                return data
            },

        },

        // ==========================================
        // ACTIONS
        // ==========================================
        actions: {

            async load() {

                try {

                    this.loading = true

                    this.error = null

                    const response =
                        await api.get(
                            "/products/",
                            {
                                params: {
                                    type: "card",
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

                    this.items =
                        list.map(
                            (item) => ({

                                ...item,

                                bank_name:
                                    item.bank_name ||
                                    item.bank?.name ||
                                    "Unknown Bank",

                                currency:
                                    String(
                                        item.currency ||
                                        item.raw_data?.currency ||
                                        ""
                                    ).toUpperCase(),

                                card_system:
                                    String(
                                        item.raw_data?.card_system ||
                                        item.card_system ||
                                        ""
                                    ).toUpperCase(),

                                validity_period:
                                    item.raw_data?.validity_period ||
                                    item.validity_period ||
                                    null,

                                issue_cost:
                                    item.raw_data?.issue_cost ||
                                    item.issue_cost ||
                                    null,
                            })
                        )

                    console.log(
                        "CARDS:",
                        this.items.length
                    )

                    console.log(
                        "FILTER SAMPLE:",
                        this.items
                            .slice(0, 20)
                            .map(x => ({
                                bank: x.bank_name,
                                currency: x.currency,
                                system: x.card_system
                            }))
                    )

                } catch (error) {

                    console.error(
                        "Cards load failed",
                        error
                    )

                    this.error =
                        error?.response?.data ||
                        error?.message ||
                        "Failed to load cards"

                    this.items = []

                } finally {

                    this.loading = false
                }
            },

            reset() {

                this.items = []

                this.loading = false

                this.error = null

                this.filters = {

                    search: "",

                    bank: null,

                    currency: "all",

                    system: "all",

                    online: false,
                }

                this.sort = "bank"
            },

        },
    }
)