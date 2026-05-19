# Task 4: Insights and Recommendations

> Based on sentiment analysis of ~1,820 Google Play reviews across CBE, BOA, and Dashen Bank.
> Model: `distilbert-base-uncased-finetuned-sst-2-english` | Themes: TF-IDF keyword matching

---

## Summary Statistics

| Bank   | Avg Rating | % Positive | % Negative | Top Pain Theme | Top Strength  |
|--------|-----------|------------|------------|----------------|---------------|
| BOA    | ~3.0 ★    | ~35%       | ~64%       | Login Issues   | Transactions  |
| CBE    | ~3.85 ★   | ~56%       | ~43%       | Performance    | UI/UX         |
| Dashen | ~3.97 ★   | ~58%       | ~41%       | Transactions   | UI/UX         |

**Overall:** 51% POSITIVE · 49% NEGATIVE · <1% NEUTRAL across all three banks combined.
Near-parity indicates none of the three banks has established a dominant positive reputation.

---

## Bank of Abyssinia (BOA)

### Satisfaction Drivers

1. **Brand trust & core transfers** — Positive reviews frequently cite BOA's established reputation and report high satisfaction when fund transfers complete successfully. Users who navigate the app without login issues give 4–5 star ratings referencing reliable bill payment and transfer functionality.

2. **Feature awareness** — Several reviews praise specific features like utility bill payment integration, indicating that when the app works, it meets user expectations for core banking tasks.

### Pain Points

1. **Login & OTP failures (critical)** — BOA has the highest concentration of negative reviews among all three banks. OTP delivery failures, session timeouts, and account lockouts are cited most frequently. Users report no clear recovery path when OTP delivery fails, leading to abandonment.
   - *Evidence:* Login Issues theme + negative sentiment cluster heavily in BOA reviews; "otp", "login", "password" are top TF-IDF keywords in BOA's negative segment.

2. **Application stability** — Crash and freeze complaints appear disproportionately in BOA reviews relative to CBE and Dashen. Performance theme keywords (slow, crash, freeze, bug) cluster in BOA's negative segment, suggesting systemic stability issues on either the client or backend side.
   - *Evidence:* BOA's average rating of ~3.0 is the lowest of the three banks; bimodal rating distribution skewed toward 1-star.

### Recommendations

1. **[Priority 1 — Complaint Management]** Overhaul the OTP delivery pipeline. Implement SMS fallback, an in-app OTP resend button with countdown timer, and clear human-readable error messages when OTP delivery fails. *Target:* reduce login-failure reviews by 40% within two release cycles.

2. **[Priority 2 — User Retention]** Integrate crash reporting (e.g., Firebase Crashlytics) with a P1 SLA for crashes affecting >1% of daily active users. Publish a public-facing fix log so users can see stability improvements in real time.

3. **[Priority 3 — Feature Enhancement]** Add biometric login (fingerprint / Face ID) as a primary authentication path to reduce OTP dependency and improve login success rate for returning users.

---

## Commercial Bank of Ethiopia (CBE)

### Satisfaction Drivers

1. **Transaction reliability** — CBE users frequently cite successful fund transfers and utility payments as the primary source of satisfaction. The transfer flow appears more stable than BOA, contributing to CBE's higher positive sentiment and better average rating (~3.85 ★).

2. **UI familiarity** — Returning users appreciate interface consistency. CBE's UI/UX theme receives relatively more positive mentions than competitors, suggesting that past design investment has resonated with the user base.

### Pain Points

1. **Performance under load** — Negative reviews frequently mention slow loading and request timeouts during high-traffic periods such as salary payment days and national holidays. The Performance theme is CBE's most common negative theme.
   - *Evidence:* "slow", "load", "freeze" appear in CBE's TF-IDF keyword set; negative reviews spike around performance keywords more than login keywords, distinguishing CBE from BOA.

2. **Customer support responsiveness** — Users escalating in-app issues report slow or unhelpful responses from support channels. The Customer Support theme appears disproportionately in CBE's negative reviews.
   - *Evidence:* "support", "response", "help" keywords in negative segment; users explicitly state they contacted support without resolution before writing the review.

### Recommendations

1. **[Priority 1 — User Retention]** Implement autoscaling infrastructure for peak-load periods. Conduct load testing at 3× typical daily active users with special attention to salary disbursement days. Add a real-time server status banner visible in-app during degraded performance windows.

2. **[Priority 2 — Complaint Management]** Deploy an AI-powered first-response chatbot covering the top 10 support query types (balance inquiry, failed transaction, card blocking, etc.). Target a <2-minute first-response time for Tier-1 issues to reduce support-themed negative reviews.

3. **[Priority 3 — Feature Enhancement]** Introduce scheduled transfers and recurring payment functionality — features that appear in positive feature-request reviews — to increase engagement among power users and reduce competitor churn.

---

## Dashen Bank

### Satisfaction Drivers

1. **Modern UI/UX** — Dashen's Super App branding and interface receive the most UI/UX-positive mentions of all three banks. Users praise intuitive navigation and modern visual design, reflecting strong mobile-first product investment.

2. **Highest average rating** — Dashen leads with ~3.97 ★ average and the most favorable positive/negative ratio (~58%/~41%). Users who engage regularly report a more consistently positive experience than peers at CBE or BOA.

### Pain Points

1. **Transaction failures** — Despite a strong UI, Dashen's negative reviews cluster around failed or delayed transactions. Users report transfers appearing to succeed but funds not arriving, creating trust issues that can drive high-value customers away.
   - *Evidence:* "transfer", "transaction", "send" keywords dominate Dashen's negative TF-IDF segment; sentiment analysis flags these reviews as strongly NEGATIVE despite generally positive UI comments.

2. **Onboarding friction** — New-user reviews mention difficulty completing initial registration and KYC verification, particularly around document upload and identity verification steps.
   - *Evidence:* Onboarding-related terms appear in low-rating first reviews; these users never progress to transactional reviews, representing silent churn at the top of the funnel.

### Recommendations

1. **[Priority 1 — User Retention]** Implement real-time transaction status notifications with clear SUCCESS / FAILED / PENDING states and an estimated resolution time. Add an in-app transaction dispute flow so users can flag failed transfers without visiting a branch.

2. **[Priority 2 — Feature Enhancement]** Redesign the onboarding flow with progressive disclosure — collect only essential information upfront and defer optional KYC steps. Benchmark completion rate before and after the redesign; target >80% onboarding completion.

3. **[Priority 3 — Complaint Management]** Leverage Dashen's UI advantage by building a proactive in-app feedback loop: prompt users who give 4–5 ★ in-app ratings to leave a Play Store review, amplifying Dashen's already-favorable sentiment signal.

---

## Ethical Considerations

| Bias Type          | Description                                                                                     | Mitigation                                              |
|--------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| Negativity bias    | Frustrated users over-index in review populations vs. satisfied silent majority                 | Treat findings as directional, not population-level     |
| Language bias      | `lang='en'` excludes Amharic reviews — potentially the majority of BOA/Dashen users            | Future sprint: extend scraping to `lang='am'`           |
| Recency bias       | Sorting by newest skews dataset toward current product state; historical trends not captured    | Broaden date range in follow-up collection              |
| Domain mismatch    | DistilBERT trained on movie reviews; banking terminology (OTP, USSD) may reduce accuracy        | Fine-tune on labelled banking reviews for production use |
| Platform bias      | Only Google Play captured; iOS App Store and social media complaints excluded                   | Add App Store scraping in Task 1 follow-up              |

> **Responsible use:** Review data must not be used to identify or profile individual users. All scraping complies with Google Play Terms of Service.

---

## Visualizations

All charts generated by `scripts/visualizations.py` and saved to `outputs/`:

| File                      | Description                                    |
|---------------------------|------------------------------------------------|
| `sentiment_distribution.png` | Overall POSITIVE / NEGATIVE / NEUTRAL counts   |
| `sentiment_by_bank.png`   | Grouped bar chart by bank and sentiment label  |
| `rating_distribution.png` | Overlapping histograms of star ratings per bank|
| `average_rating.png`      | Average star rating per bank                   |
| `theme_frequency.png`     | Horizontal bar chart of theme counts           |

See `reports/Omega_Consultancy_Final_Report.pdf` for the full stakeholder report with embedded visualizations.