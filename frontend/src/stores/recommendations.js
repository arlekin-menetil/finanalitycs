import { defineStore } from "pinia"
import api from "@/api/axios"

export const useRecommendationsStore = defineStore(
  "recommendations",
  {
    // ==========================================
    // STATE
    // ==========================================

    state: () => ({
      recommendations: [],
      products: [],
      topBanks: [],
      snapshotId: null,
      rankingVersion: null,
      marketRating: [],
      totalBanks: 0,

      loading: {
        recommendations: false,
        products: false,
        rating: false,
        topBanks: false,
      },

      error: null,
    }),

    // ==========================================
    // GETTERS
    // ==========================================

    getters: {
      topRecommendations: (state) => {
        return [...state.recommendations]
          .sort(
            (a, b) =>
              Number(b.ranking_score || 0) -
              Number(a.ranking_score || 0)
          )
          .slice(0, 5)
      },

      allProducts: (state) => {
        return state.products
      },

      filteredProducts: (state) => {
        return (type = null) => {
          if (!type) {
            return state.products
          }

          return state.products.filter(
            (product) =>
              String(product.product_type)
                .toLowerCase() ===
              String(type)
                .toLowerCase()
          )
        }
      },

      hasData: (state) => {
        return (
          state.products.length > 0 ||
          state.recommendations.length > 0
        )
      },
    },

    // ==========================================
    // ACTIONS
    // ==========================================

    actions: {
      // ==========================================
      // SAFE NUMBER
      // ==========================================

      safeNumber(value, fallback = 0) {
        if (
          value === null ||
          value === undefined ||
          value === ""
        ) {
          return fallback
        }

        const parsed = Number(
          String(value)
            .replace(",", ".")
            .replace(/\s+/g, "")
        )

        return Number.isFinite(parsed)
          ? parsed
          : fallback
      },

      // ==========================================
      // SAFE ARRAY
      // ==========================================

      safeArray(value) {
        return Array.isArray(value)
          ? value
          : []
      },

      // ==========================================
      // SAFE BOOLEAN
      // ==========================================

      safeBoolean(value) {
        return Boolean(value)
      },

      // ==========================================
      // NORMALIZE BANK NAME
      // ==========================================

      normalizeBankName(bankName) {
        if (!bankName) {
          return "Unknown Bank"
        }

        const value =
          String(bankName)
            .trim()
            .replace(/\s+/g, " ")

        const lower = value.toLowerCase()

        if (
          lower.includes("sqb") ||
          lower.includes("узпромстрой") ||
          lower.includes("uzpromstroy")
        ) {
          return "SQB"
        }

        if (
          lower.includes("nbu") ||
          lower.includes("national bank")
        ) {
          return "NBU"
        }

        if (lower.includes("xalq")) {
          return "Xalq Banki"
        }

        if (lower.includes("ipak")) {
          return "Ipak Yuli Bank"
        }

        if (lower.includes("agrobank")) {
          return "Agrobank"
        }

        if (lower.includes("asaka")) {
          return "Asaka Bank"
        }

        if (lower.includes("kapital")) {
          return "Kapitalbank"
        }

        if (lower.includes("hamkor")) {
          return "Hamkorbank"
        }

        if (lower.includes("aloqa")) {
          return "Aloqabank"
        }

        if (lower.includes("orient")) {
          return "Orient Finans"
        }

        return value
      },

      // ==========================================
      // NORMALIZE SCORE
      // ==========================================

      normalizeScore(value) {
        const score = this.safeNumber(value)

        if (score <= 1) {
          return Math.round(score * 100)
        }

        return Math.round(score)
      },

      // ==========================================
      // NORMALIZE APPROVAL
      // ==========================================

      normalizeProbability(value) {
        const probability =
          this.safeNumber(value)

        if (probability <= 1) {
          return Math.round(
            probability * 100
          )
        }

        return Math.round(probability)
      },

      // ==========================================
      // NORMALIZE PRODUCT
      // ==========================================

      normalizeProduct(
        item,
        index = 0
      ) {
        if (!item) {
          return null
        }

        const bankName =
          this.normalizeBankName(
            item.bank_name ||
            item.bank?.name ||
            item.bank ||
            item.best_bank ||
            "Unknown Bank"
          )

        const rankingScore =
          this.normalizeScore(
            item.ranking_score ??
            item.score ??
            0
          )

        const approvalProbability =
          this.normalizeProbability(
            item.approval_probability ??
            item.approvalProbability ??
            0
          )

        const interestRate =
          this.safeNumber(
            item.interest_rate,
            null
          )

        const maxAmount =
          this.safeNumber(
            item.max_amount ??
            item.loan_limit_hint,
            null
          )

        const priority =
          this.safeNumber(
            item.priority,
            0
          )

        const featured =
          this.safeBoolean(
            item.featured ??
            item.is_featured ??
            false
          )

        const online =
          this.safeBoolean(
            item.real_online ??
            item.is_online ??
            false
          )

        const productType =
          String(
            item.product_type ||
            item.loan_type ||
            "loan"
          ).toLowerCase()

        return {
          // ======================================
          // IDS
          // ======================================

          id:
            item.id ||
            item.product_id ||
            index,

          bank_id:
            item.bank_id ||
            item.bank?.id ||
            null,

          // ======================================
          // BANK
          // ======================================

          bank_name:
            bankName,

          bank:
            item.bank ||
            null,

          // ======================================
          // PRODUCT
          // ======================================

          product_name:
            item.product_name ||
            item.name ||
            "Кредит",

          product_type:
            productType,

          loan_type:
            productType,

          description:
            item.description ||
            null,

          // ======================================
          // FINANCE
          // ======================================

          interest_rate:
            interestRate,

          min_rate:
            this.safeNumber(
              item.min_rate,
              null
            ),

          max_rate:
            this.safeNumber(
              item.max_rate,
              null
            ),

          max_amount:
            maxAmount,

          loan_limit_hint:
            maxAmount,

          term:
            this.safeNumber(
              item.term,
              null
            ),

          currency:
            item.currency ||
            "UZS",

          // ======================================
          // AI
          // ======================================

          ranking_score:
            rankingScore,

          approval_probability:
            approvalProbability,

          priority:
            priority,

          featured:
            featured,

          is_featured:
            featured,

          // ======================================
          // ONLINE
          // ======================================

          real_online:
            online,

          is_online:
            online,

          // ======================================
          // EXTRA
          // ======================================

          offers_count:
            this.safeNumber(
              item.offers_count,
              1
            ),

          banks_count:
            this.safeNumber(
              item.banks_count,
              1
            ),

          website:
            item.website ||
            item.source_url ||
            item.bank_url ||
            null,

          source_url:
            item.source_url ||
            null,

          explanations:
            this.safeArray(
              item.explanations
            ),
        }
      },
      // ==========================================
      // LOAD RECOMMENDATIONS
      // ==========================================

      async loadRecommendations(
        limit = 500,
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

          const { data } = await api.get(
            "/banks/recommendations/",
            {
              params: {
                limit,
              },
            }
          )

          this.snapshotId =
            data?.snapshot_id ??
            data?.snapshotId ??
            null

          this.rankingVersion =
            data?.ranking_version ??
            data?.rankingVersion ??
            null

          let list = []

          if (Array.isArray(data)) {
            list = data
          } else {
            list =
              data?.recommendations ||
              data?.results ||
              []
          }

          const normalized =
            this.removeDuplicates(
              list
                .map((item, index) => {
                  return this.normalizeProduct(
                    {
                      ...item,
                      ...(item.product || {}),
                    },
                    index
                  )
                })
                .filter((product) => {
                  return (
                    product &&
                    product.bank_name &&
                    product.bank_name !==
                    "Unknown Bank"
                  )
                })
            )

          // ======================================
          // SORT RECOMMENDATIONS
          // ======================================

          normalized.sort((a, b) => {
            // Featured
            if (
              a.featured !==
              b.featured
            ) {
              return (
                Number(b.featured) -
                Number(a.featured)
              )
            }

            // Priority
            if (
              a.priority !==
              b.priority
            ) {
              return (
                b.priority -
                a.priority
              )
            }

            // AI Score
            if (
              a.ranking_score !==
              b.ranking_score
            ) {
              return (
                b.ranking_score -
                a.ranking_score
              )
            }

            // Approval
            if (
              a.approval_probability !==
              b.approval_probability
            ) {
              return (
                b.approval_probability -
                a.approval_probability
              )
            }

            // Interest
            return (
              Number(
                a.interest_rate || 999
              ) -
              Number(
                b.interest_rate || 999
              )
            )
          })

          this.recommendations =
            normalized

          this.totalBanks =
            new Set(
              normalized.map(
                (item) =>
                  item.bank_name
              )
            ).size

          console.log(
            "Recommendations:",
            normalized.length
          )

          console.log(
            "Banks:",
            this.totalBanks
          )
        } catch (error) {
          console.error(
            "Recommendations error:",
            error
          )

          this.error =
            error?.response?.data ||
            error.message ||
            "Failed to load recommendations"

          this.recommendations = []
          this.totalBanks = 0
        } finally {
          this.loading.recommendations =
            false
        }
      },
      // ==========================================
      // LOAD TOP BANKS
      // ==========================================

      async loadTopBanks(
        force = false
      ) {
        if (
          this.topBanks.length &&
          !force
        ) {
          return
        }

        try {
          this.loading.topBanks = true
          this.error = null

          // Загружаем все рекомендации
          await this.loadRecommendations(
            500,
            force
          )

          const grouped = {}

          for (
            const item of this.recommendations
          ) {
            const bankName =
              item.bank_name ||
              "Unknown Bank"

            if (
              bankName ===
              "Unknown Bank"
            ) {
              continue
            }

            if (!grouped[bankName]) {
              grouped[bankName] = {
                bank_id:
                  item.bank_id,

                bank_name:
                  bankName,

                featured:
                  Boolean(
                    item.featured ??
                    item.is_featured
                  ),

                priority:
                  Number(
                    item.priority || 0
                  ),

                offers: 0,

                totalScore: 0,

                totalApproval: 0,

                avgScore: 0,

                avgApproval: 0,

                maxScore: 0,

                minScore: 100,

                bestProduct: null,

                products: [],
              }
            }

            const bank =
              grouped[bankName]

            const score =
              Number(
                item.ranking_score || 0
              )

            const approval =
              Number(
                item.approval_probability ||
                0
              )

            bank.offers++

            bank.totalScore +=
              score

            bank.totalApproval +=
              approval

            bank.maxScore =
              Math.max(
                bank.maxScore,
                score
              )

            bank.minScore =
              Math.min(
                bank.minScore,
                score
              )

            // featured
            if (
              item.featured ||
              item.is_featured
            ) {
              bank.featured = true
            }

            // priority
            bank.priority =
              Math.max(
                bank.priority,
                Number(
                  item.priority || 0
                )
              )

            // лучший продукт банка
            if (
              !bank.bestProduct ||
              score >
              Number(
                bank.bestProduct
                  .ranking_score || 0
              )
            ) {
              bank.bestProduct =
                item
            }

            bank.products.push(
              item
            )
          }

          const result =
            Object.values(grouped)
              .map((bank) => {
                // ======================================
                // AVERAGE AI SCORE
                // ======================================

                bank.avgScore =
                  Math.round(
                    bank.totalScore /
                    Math.max(
                      bank.offers,
                      1
                    )
                  )

                // ======================================
                // AVERAGE APPROVAL
                // ======================================

                bank.avgApproval =
                  Math.round(
                    bank.totalApproval /
                    Math.max(
                      bank.offers,
                      1
                    )
                  )

                // ======================================
                // IMPORTANT
                // ======================================
                // RecommendationsView.vue
                // использует именно ranking_score
                //
                // Поэтому передаём средний
                // AI-рейтинг банка туда.
                bank.ranking_score =
                  bank.avgScore

                // Для совместимости
                // оставляем также score.
                bank.score =
                  bank.avgScore

                // ======================================
                // SORT PRODUCTS
                // ======================================

                bank.products.sort(
                  (a, b) =>
                    Number(
                      b.ranking_score || 0
                    ) -
                    Number(
                      a.ranking_score || 0
                    )
                )

                return bank
              })

              // ======================================
              // SORT BANKS
              // ======================================

              .sort((a, b) => {
                // FEATURED
                if (
                  a.featured !==
                  b.featured
                ) {
                  return (
                    Number(b.featured) -
                    Number(a.featured)
                  )
                }

                // PRIORITY
                if (
                  a.priority !==
                  b.priority
                ) {
                  return (
                    b.priority -
                    a.priority
                  )
                }

                // AI SCORE
                if (
                  a.avgScore !==
                  b.avgScore
                ) {
                  return (
                    b.avgScore -
                    a.avgScore
                  )
                }

                // APPROVAL
                if (
                  a.avgApproval !==
                  b.avgApproval
                ) {
                  return (
                    b.avgApproval -
                    a.avgApproval
                  )
                }

                // OFFERS
                return (
                  b.offers -
                  a.offers
                )
              })

          this.topBanks = result

          console.log(
            "TOP BANKS:",
            result
          )
        } catch (error) {
          console.error(
            "Top banks error:",
            error
          )

          this.error =
            error?.response?.data ||
            error.message ||
            "Failed to load top banks"

          this.topBanks = []
        } finally {
          this.loading.topBanks =
            false
        }
      },
      // ==========================================
      // REMOVE DUPLICATES
      // ==========================================

      removeDuplicates(
        items = []
      ) {
        const seen = new Set()

        return items.filter(
          (item) => {
            const key = [
              item.bank_name,
              item.product_name,
              item.product_type,
              item.interest_rate,
              item.term,
            ].join("|")

            if (seen.has(key)) {
              return false
            }

            seen.add(key)

            return true
          }
        )
      },

      // ==========================================
      // LOAD PRODUCTS
      // ==========================================

      async loadProducts({
        type = null,
        bank_type = null,
        limit = 500,
        append = false,
        force = false,
      } = {}) {
        if (
          this.products.length &&
          !force &&
          !append &&
          !type &&
          !bank_type
        ) {
          return
        }

        try {
          this.loading.products = true
          this.error = null

          const params = {
            limit,
          }

          if (type) {
            params.type = type
          }

          if (bank_type) {
            params.bank_type =
              bank_type
          }

          const { data } =
            await api.get(
              "/banks/products/",
              {
                params,
              }
            )

          let list = []

          if (Array.isArray(data)) {
            list = data
          } else {
            list =
              data?.results ||
              data?.products ||
              []
          }

          const normalized =
            this.removeDuplicates(
              list
                .map(
                  (item, index) =>
                    this.normalizeProduct(
                      item,
                      index
                    )
                )
                .filter(Boolean)
            )

          if (append) {
            this.products = [
              ...this.products,
              ...normalized,
            ]
          } else {
            this.products =
              normalized
          }
        } catch (error) {
          console.error(error)

          this.error =
            error?.response?.data ||
            error.message ||
            "Failed to load products"

          this.products = []
        } finally {
          this.loading.products =
            false
        }
      },

      // ==========================================
      // REFRESH ALL
      // ==========================================

      async refreshAll() {
        this.reset()

        await Promise.all([
          this.loadProducts({
            force: true,
            limit: 500,
          }),

          this.loadRecommendations(
            500,
            true
          ),
        ])

        await this.loadTopBanks(true)
      },

      // ==========================================
      // RESET
      // ==========================================

      reset() {
        this.recommendations = []

        this.products = []

        this.topBanks = []

        this.marketRating = []

        this.snapshotId = null

        this.rankingVersion = null

        this.totalBanks = 0

        this.error = null

        this.loading = {
          recommendations: false,
          products: false,
          rating: false,
          topBanks: false,
        }
      },
    },
  }
)