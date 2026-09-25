import { defineStore } from "pinia"
import api from "@/api/axios"

export const useBanksStore = defineStore(

  "banks",

  {

    // ==========================================
    // 💣 STATE
    // ==========================================
    state: () => ({

      // ==========================================
      // 🏦 BANKS
      // ==========================================
      banks: [],

      total: 0,

      // ==========================================
      // 💣 PRODUCTS
      // ==========================================
      products: [],

      aggregated: [],

      recommendations: [],

      // ==========================================
      // 🏢 BRANCHES
      // ==========================================
      branches: [],

      mapBranches: [],

      // ==========================================
      // 💣 FILTERS
      // ==========================================
      selectedType: null,

      selectedSort: "min_rate",

      // ==========================================
      // 🔄 LOADING
      // ==========================================
      loading: {

        banks: false,

        products: false,

        recommendations: false,

        branches: false,

        map: false,
      },

      // ==========================================
      // ❌ ERROR
      // ==========================================
      error: null,
    }),

    // ==========================================
    // 🧠 GETTERS
    // ==========================================
    getters: {

      // ==========================================
      // 💣 HAS RECOMMENDATIONS
      // ==========================================
      hasRecommendations: (state) => {

        return (
          state.recommendations.length > 0
        )
      },

      // ==========================================
      // 🔥 TOP RECOMMENDATIONS
      // ==========================================
      topRecommendations: (state) => {

        return [

          ...state.recommendations

        ]

          .sort((a, b) => {

            return (

              Number(b.ranking_score || 0)

              -

              Number(a.ranking_score || 0)
            )
          })

          .slice(0, 5)
      },

      // ==========================================
      // 💣 ALL PRODUCTS
      // ==========================================
      allProducts: (state) => {

        return state.products
      },
    },

    // ==========================================
    // 🚀 ACTIONS
    // ==========================================
    actions: {

      // ==========================================
      // 💣 SAFE NUMBER
      // ==========================================
      safeNumber(
        value,
        fallback = 0
      ) {

        const num = Number(value)

        return Number.isFinite(num)

          ? num

          : fallback
      },

      // ==========================================
      // 💣 NORMALIZER
      // ==========================================
      normalizeProduct(
        item,
        index = 0
      ) {

        if (!item) {

          return null
        }

        const ranking = this.safeNumber(

          item.ranking_score ??

          item.score ??

          0
        )

        const probability = this.safeNumber(

          item.approval_probability ??

          item.approvalProbability ??

          0
        )

        const finalRanking =

          ranking <= 1

            ? Math.round(
              ranking * 100
            )

            : Math.round(
              ranking
            )

        const finalProbability =

          probability <= 1

            ? Math.round(
              probability * 100
            )

            : Math.round(
              probability
            )

        const bankName = (

          item.bank_name ||

          item.best_bank ||

          item.bank?.name ||

          "Unknown Bank"
        )

        return {

          // ==========================================
          // 💣 IDS
          // ==========================================
          id:

            item.id ||

            item.product_id ||

            index,

          bank_id:

            item.bank_id ||

            item.bank?.id ||

            null,

          // ==========================================
          // 💣 BANK
          // ==========================================
          bank_name: bankName,

          // ==========================================
          // 💣 PRODUCT
          // ==========================================
          product_name:

            item.product_name ||

            item.name ||

            item.category ||

            "Кредит",

          // ==========================================
          // 💣 TYPES
          // ==========================================
          product_type:

            item.product_type ||

            item.loan_type ||

            "loan",

          // ==========================================
          // 💣 RATE
          // ==========================================
          interest_rate:

            item.interest_rate ??

            item.best_rate ??

            null,

          min_rate:

            item.min_rate ??

            null,

          max_rate:

            item.max_rate ??

            null,

          // ==========================================
          // 💣 LIMIT
          // ==========================================
          loan_limit_hint:

            item.loan_limit_hint ||

            item.max_amount ||

            null,

          // ==========================================
          // 💣 TERM
          // ==========================================
          term:

            item.term ||

            null,

          // ==========================================
          // 💣 ONLINE
          // ==========================================
          is_online:

            Boolean(
              item.is_online
            ),

          // ==========================================
          // 💣 SCORING
          // ==========================================
          ranking_score:

            finalRanking,

          approval_probability:

            finalProbability,

          // ==========================================
          // 💣 META
          // ==========================================
          offers_count:

            item.offers_count ||

            1,

          banks_count:

            item.banks_count ||

            1,

          // ==========================================
          // 💣 URL
          // ==========================================
          website:

            item.website ||

            item.source_url ||

            item.bank_url ||

            null,

          // ==========================================
          // 💣 FEATURED
          // ==========================================
          is_featured:

            Boolean(
              item.is_featured
            ),

          // ==========================================
          // 💣 TAGS
          // ==========================================
          explanations:

            item.explanations ||

            [],

          description:

            item.description ||

            null,
        }
      },

      // ==========================================
      // 🏦 LOAD BANKS
      // ==========================================
      async loadBanks(
        search = "",
        force = false
      ) {

        if (
          this.banks.length &&
          !search &&
          !force
        ) {
          return
        }

        try {

          this.loading.banks = true

          this.error = null

          const res = await api.get(

            "/banks/",

            {
              params: { search }
            }
          )

          const data =
            res?.data || {}

          const list =

            data.banks ||

            data.results ||

            data ||

            []

          this.banks = Array.isArray(list)

            ? list

            : []

          this.total =

            data.total ||

            this.banks.length

        } catch (e) {

          console.error(
            "Banks error:",
            e
          )

          this.error = (

            e?.response?.data ||

            e.message ||

            "Banks error"
          )

        } finally {

          this.loading.banks = false
        }
      },
      // ==========================================
      // 💣 LOAD PRODUCTS
      // ==========================================
      async loadProducts(
        {
          force = false
        } = {}
      ) {

        if (
          this.products.length &&
          !force
        ) {
          return
        }

        try {

          this.loading.products = true

          this.error = null

          const params = {}

          // ==========================================
          // 💣 TYPE FILTER
          // ==========================================
          if (this.selectedType) {

            params.type =
              this.selectedType
          }

          // ==========================================
          // 💣 SORTING
          // ==========================================
          if (
            this.selectedSort ===
            "min_rate"
          ) {

            params.ordering =
              "interest_rate"
          }

          if (
            this.selectedSort ===
            "max_rate"
          ) {

            params.ordering =
              "-interest_rate"
          }

          if (
            this.selectedSort ===
            "offers"
          ) {

            params.ordering =
              "-offers_count"
          }

          params.limit = 500

          const res = await api.get(

            "/banks/products/",

            { params }
          )

          const data =
            res?.data || {}

          let list = []

          if (Array.isArray(data)) {

            list = data

          } else {

            list =

              data.results ||

              data.products ||

              []
          }

          // ==========================================
          // 💣 REMOVE CARDS
          // ==========================================
          list = list.filter((item) => {

            const type = (

              item.product_type ||

              item.loan_type ||

              ""
            ).toLowerCase()

            return ![
              "card",
              "credit_card",
              "debit_card",
              "deposit",
            ].includes(type)
          })

          this.products = list

            .map((item, index) => {

              return this.normalizeProduct(
                item,
                index
              )
            })

            .filter(Boolean)

        } catch (e) {

          console.error(
            "Products error:",
            e
          )

          this.error = (

            e?.response?.data ||

            e.message ||

            "Products error"
          )

          this.products = []

        } finally {

          this.loading.products = false
        }
      },

      // ==========================================
      // 💣 LOAD AGGREGATED
      // ==========================================
      async loadAggregated() {

        try {

          const res = await api.get(
            "/banks/products/aggregated/"
          )

          const data =
            res?.data || {}

          let list = []

          if (Array.isArray(data)) {

            list = data

          } else {

            list =

              data.results ||

              data.products ||

              []
          }

          this.aggregated = list

            .map((item, index) => {

              return this.normalizeProduct(
                item,
                index
              )
            })

            .filter(Boolean)

        } catch (e) {

          console.error(
            "Aggregated error:",
            e
          )
        }
      },

      // ==========================================
      // 💣 SET TYPE
      // ==========================================
      setType(type) {

        this.selectedType = type

        this.loadProducts({
          force: true
        })
      },

      // ==========================================
      // 💣 SET SORT
      // ==========================================
      setSort(sort) {

        this.selectedSort = sort

        this.loadProducts({
          force: true
        })
      },

      // ==========================================
      // 💣 LOAD RECOMMENDATIONS
      // ==========================================
      async loadRecommendations(
        force = false
      ) {

        if (
          this.recommendations.length &&
          !force
        ) {
          return
        }

        try {

          this.loading.recommendations = true

          this.error = null

          const res = await api.get(
            "/banks/recommendations/"
          )

          const data =
            res?.data || {}

          let list = []

          if (Array.isArray(data)) {

            list = data

          } else {

            list =

              data.recommendations ||

              data.results ||

              []
          }

          // ==========================================
          // 💣 REMOVE CARDS
          // ==========================================
          list = list.filter((item) => {

            const product =
              item.product || item

            const type = (

              product.product_type ||

              product.loan_type ||

              ""
            ).toLowerCase()

            return ![
              "card",
              "credit_card",
              "debit_card",
              "deposit",
            ].includes(type)
          })

          this.recommendations = list

            .map((item, index) => {

              const product =
                item.product || item

              const normalized =
                this.normalizeProduct(
                  product,
                  index
                )

              return {

                ...normalized,

                ranking_score:

                  Number(
                    normalized.ranking_score || 0
                  ),

                approval_probability:

                  Number(
                    normalized.approval_probability || 0
                  ),

                explanations:

                  item.explanations ||

                  normalized.explanations ||

                  [],
              }
            })

            .filter(Boolean)

            // ==========================================
            // 💣 SORT
            // ==========================================
            .sort((a, b) => {

              return (

                Number(b.ranking_score || 0)

                -

                Number(a.ranking_score || 0)
              )
            })

        } catch (e) {

          console.error(
            "Recommendations error:",
            e
          )

          this.error = (

            e?.response?.data ||

            e.message ||

            "Recommendations error"
          )

        } finally {

          this.loading.recommendations = false
        }
      },

      // ==========================================
      // 🏢 LOAD BANK BRANCHES
      // ==========================================
      async loadBranches(bankId) {

        try {

          this.loading.branches = true

          this.error = null

          const res = await api.get(
            `/banks/${bankId}/branches/`
          )

          const data =
            res?.data || {}

          this.branches =

            data.branches ||

            data.results ||

            []

        } catch (e) {

          console.error(
            "Branches error:",
            e
          )

          this.error = (

            e?.response?.data ||

            e.message ||

            "Branches error"
          )

        } finally {

          this.loading.branches = false
        }
      },

      // ==========================================
      // 🗺 LOAD MAP BRANCHES
      // ==========================================
      async loadMapBranches(
        force = false
      ) {

        if (
          this.mapBranches.length &&
          !force
        ) {
          return
        }

        try {

          this.loading.map = true

          this.error = null

          const res = await api.get(
            "/banks/branches/"
          )

          const data =
            res?.data || {}

          const list =

            data.results ||

            data.branches ||

            []

          this.mapBranches = list.map(

            (item, index) => ({

              id:
                item.id || index,

              bank_id:
                item.bank_id || null,

              bank_name:
                item.bank_name || "Банк",

              name:
                item.name || null,

              city:
                item.city || null,

              address:
                item.address || null,

              phone:
                item.phone || null,

              working_hours:
                item.working_hours || null,

              latitude:

                item.latitude ||

                item.lat ||

                null,

              longitude:

                item.longitude ||

                item.lng ||

                null,

              lat:

                item.lat ||

                item.latitude ||

                null,

              lng:

                item.lng ||

                item.longitude ||

                null,
            })
          )

        } catch (e) {

          console.error(
            "Map error:",
            e
          )

          this.error = (

            e?.response?.data ||

            e.message ||

            "Map error"
          )

        } finally {

          this.loading.map = false
        }
      },

      // ==========================================
      // 💰 CLICK
      // ==========================================
      async click(productId) {

        try {

          await api.post(

            "/banks/click/",

            {
              product_id: productId
            }
          )

        } catch (e) {

          console.error(
            "Click error:",
            e
          )
        }
      },

      // ==========================================
      // 💰 APPLY
      // ==========================================
      async apply(productId) {

        try {

          await api.post(

            "/banks/apply/",

            {
              product_id: productId
            }
          )

        } catch (e) {

          console.error(
            "Apply error:",
            e
          )
        }
      },

      // ==========================================
      // 💣 RESET
      // ==========================================
      reset() {

        this.banks = []

        this.products = []

        this.aggregated = []

        this.recommendations = []

        this.branches = []

        this.mapBranches = []

        this.total = 0

        this.selectedType = null

        this.selectedSort = "min_rate"

        this.error = null
      }
    }
  }
)