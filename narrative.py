"""Written analysis for every visual.

Each entry keeps the brief's four parts (description, insight, interpretation, recommendation) for the written
report. The dashboard shows, in research-paper style: the description of the graph, then a conclusion paragraph
(`conclusion`: findings ending in "It can be concluded that…") and a recommendation paragraph (`recommend`).
"""

# Lower level: written for 2025 Campaign 5 (the latest campaign)
LOWER = {'kpi': {'description': 'Six KPI cards summarise 2025 Campaign 5, each showing the change against the previous '
                        'campaign (2025 Campaign 4): survey responses, CSAT, NPS, Wait Time OK, Answer Satisfaction '
                        'and the number of dissatisfied callers. Each card also shows a sparkline of the last six '
                        'campaigns, so a one-campaign change can be read against the longer pattern.',
         'insight': 'CSAT is **81.9%** (on target, **+0.3 pt**) and NPS is **+56.8** (flat, +0.1). Dissatisfied '
                    'callers fell from **161 to 139 (−22)**. Two KPIs moved the wrong way: **Answer Satisfaction '
                    'slipped from 68.7% to 66.6% (−2.1 pt)** and Wait Time OK slipped from 83.7% to 82.8% (−0.9 pt).',
         'interpretation': 'Overall service is stable and above target, so there is no emergency. But Answer '
                           'Satisfaction, the one KPI clearly getting worse, is a strong driver of overall '
                           'satisfaction (r = +0.69) and NPS (r = +0.64) in the correlation analysis. If it keeps '
                           'sliding, CSAT and NPS will follow.',
         'recommendation': 'Keep the current service approach, but make **Answer Satisfaction the focus KPI** for the '
                           'next campaign. Give it its own target (for example ≥ 70%) and review it in the daily team '
                           'huddle next to CSAT.',
         'conclusion': 'The operational scorecard shows that the call center met its service baseline in 2025 Campaign '
                       '5. CSAT reached **81.9%**, above the 80% working target and 0.3 points higher than in the '
                       'previous campaign, while NPS held at **+56.8** and dissatisfied callers fell from **161 to '
                       '139**. However, Answer Satisfaction declined by **2.1 points to 66.6%**, the only key '
                       'indicator that moved materially in the wrong direction. It can therefore be concluded that '
                       'overall service is stable but the quality of the answers callers receive is weakening. Because '
                       'this driver is strongly associated with overall satisfaction (r = 0.69) and NPS (r = 0.64), '
                       'its decline poses a risk to future results.',
         'recommend': 'In light of these findings, it is recommended that floor supervisors adopt Answer Satisfaction '
                      'as a focus KPI with its own target of at least 70%, and that it be reviewed alongside CSAT in '
                      'the daily team huddle.'},
 'daily': {'description': 'The top panel is a control chart (a p-chart, the standard contact-center tool for daily '
                          "rates). Each dot is one day's CSAT; the light vertical bar behind it is that day's 3-sigma "
                          'control limits around the campaign average of 81.9%, so it is long on small days and short '
                          'on busy ones. The dashed line is the 80% target. The bottom panel shows survey responses '
                          'per day. Clicking any day opens its snapshot and filters the follow-up log; a toggle adds '
                          'the 7-day rolling CSAT.',
           'insight': '**No day in 2025 Campaign 5 falls outside its control limits**, not even Tuesday Nov 18 (66.7% '
                      'on 24 responses, against a lower limit of 58.4%). Feedback arrives in bursts: **75% of '
                      'responses came in the first 12 days**, peaking at **221 on Wednesday Nov 12**. Nov 16–19 were '
                      'four consecutive days below both the campaign average and the 80% target, the longest such run '
                      'in the campaign.',
           'interpretation': 'Day-to-day swings in this campaign are consistent with normal sampling noise, so a '
                             'single bad day is not evidence that something broke. The four-day run is worth checking '
                             'as a possible short-lived shift. The bigger issue is the campaign-wide gap in answer '
                             'quality shown in the next charts. The control chart stops supervisors from chasing noise '
                             'on small days and from missing real changes on busy ones.',
           'recommendation': 'Escalate when a day falls **outside its control limits** or when **two or more '
                             'consecutive days are below target** (as Nov 16–17 were); the alert banner above the '
                             'chart applies both rules automatically. Review the chart each morning during the first '
                             'two weeks of a campaign, when most responses arrive, and rely on the control limits '
                             'rather than raw daily percentages after that.',
           'conclusion': 'The control chart shows that **no day in 2025 Campaign 5 fell outside its statistical '
                         'control limits**, including Tuesday, November 18 (66.7% on 24 responses, against a lower '
                         'limit of 58.4%). Feedback arrived in bursts: **75% of responses were received in the first '
                         '12 days**, with a peak of **221 on Wednesday, November 12**. The only notable pattern was a '
                         'run of **four consecutive days below target from November 16 to 19**. It can be concluded '
                         'that day-to-day variation in this campaign is consistent with normal sampling noise and that '
                         'single low days do not indicate a service breakdown. The four-day run, however, suggests a '
                         'short-lived shift that merits review.',
           'recommend': 'It is recommended that supervisors escalate only when a day falls outside its control limits '
                        "or when two or more consecutive days fall below target, as the dashboard's alert banner now "
                        'does automatically. It is further recommended that the chart be reviewed every morning during '
                        'the first two weeks of each campaign, when most responses arrive.'},
 'dims': {'description': 'A diverging stacked bar shows the rating mix for each of the five survey questions. Negative '
                         'ratings (1–2) extend left of the centre line, positive ratings (4–5) extend right, and '
                         'Neutral is split across the centre. The table repeats the numbers.',
          'insight': 'Agent Customer Service is **90.6% positive / 4.5% negative** and Agent Job Knowledge is 86.5% / '
                     '5.1%. Wait Time is 82.8% / 8.4% and Overall is 81.9% / 11.3%. **Answer Satisfaction is only '
                     '66.6% positive and 16.8% negative (208 callers)**, the most negative of any question and **24 '
                     'points behind agent service**. Among low-score responses where the four drivers were rated '
                     'differently, Answer Satisfaction was the lowest (or tied-lowest) rating **76.8% of the time**.',
          'interpretation': 'Callers rate the *people* well but the *outcome* poorly. The agent is courteous and '
                            'knowledgeable, yet the answer (the information, the policy or the next step) does not '
                            'satisfy the caller. Because answer satisfaction is a top driver of overall satisfaction '
                            'and NPS, it is the biggest lever available to front-line supervisors. Wait time is the '
                            'second weakest area.',
          'recommendation': 'QA leads should pull a **weekly sample of calls rated Answer 1–2** to find the recurring '
                            'topics behind them, then update the knowledge-base articles and call scripts for those '
                            'topics. Coach agents to explain **what happens next** (timelines, which agency handles '
                            'it, how to track the request) when the answer cannot be what the caller hoped for.',
          'conclusion': 'The rating mix shows a clear gap between how callers rate the agents and how they rate the '
                        'outcome. Agent Customer Service received **90.6% positive** ratings and Agent Job Knowledge '
                        '86.5%, whereas Answer Satisfaction received only **66.6% positive and 16.8% negative** '
                        'ratings (208 callers), a 24-point gap. Among low-score responses, Answer Satisfaction was the '
                        'lowest-rated driver **76.8% of the time**. It can therefore be concluded that dissatisfaction '
                        'stems mainly from the information, policy or next step given to callers rather than from '
                        'agent courtesy or competence.',
          'recommend': 'It is recommended that QA leads review a weekly sample of calls rated 1–2 on Answer '
                       'Satisfaction to identify recurring topics, update the knowledge base and call scripts for '
                       'those topics, and coach agents to explain clearly what happens next when the answer cannot '
                       "meet the caller's expectation."},
 'queues': {'description': 'A dot-and-whisker chart compares the four language queues (English, Spanish, Chinese, '
                           "Others) on CSAT and Answer Satisfaction. Each dot is the queue's % positive and the "
                           'whisker is its 95% confidence interval (Wilson), so a wide whisker means few responses. '
                           'The dashed line is the CSAT target. The table adds volume share, Wait and Agent Service '
                           'ratings, NPS and dissatisfied callers.',
            'insight': 'The **English queue handles 75.5% of responses** and is the only queue below target at '
                       '**79.5%**, but its interval (76.8–82.0%) includes 80%, so the gap is borderline. It still '
                       'accounts for **120 of the 139 dissatisfied callers (86%)**. **Spanish is clearly better**: '
                       'CSAT 90.8% (86.0–94.1%), an interval that does not overlap English. The **Others queue** (n = '
                       '42) has Answer Satisfaction of **35.7% (23.0–50.8%)**; even with its small sample, that is '
                       'clearly below English (61.1–67.2%). Chinese (n = 64) looks strong, but its interval is wide '
                       '(79.1–94.6%).',
            'interpretation': "English carries three-quarters of the volume, so it drives most of the campaign's "
                              'dissatisfaction even though its gap to target is within the margin of error. Two '
                              'findings are statistically clear: Spanish outperforms, and Others has an answer-quality '
                              'problem. Those are the ones to act on. The confidence intervals keep the team from '
                              'over-reading small queues.',
            'recommendation': 'Run peer-learning sessions that pair English-queue agents with top Spanish-queue '
                              'agents, and put the English queue first in the weekly QA sample. Treat the Others '
                              "queue's answer problem as real despite its size: review interpreter and language-line "
                              'handoffs this campaign.',
            'conclusion': 'The queue comparison shows that the English queue, which handled **75.5% of responses**, '
                          'was the only queue below the CSAT target at **79.5%**, although its 95% confidence interval '
                          '(76.8–82.0%) includes the target. It nevertheless accounted for **120 of the 139 '
                          'dissatisfied callers (86%)**. The Spanish queue performed significantly better, with CSAT '
                          'of **90.8%** (86.0–94.1%), and the Others queue had a significantly lower Answer '
                          'Satisfaction of **35.7%** (23.0–50.8%) despite its small sample. It can be concluded that '
                          'the English queue drives most dissatisfaction because of its volume, while the Spanish '
                          "advantage and the Others queue's answer-quality problem are statistically clear.",
            'recommend': 'It is recommended that team leads pair English-queue agents with top Spanish-queue agents '
                         'for peer learning, prioritise the English queue in the weekly QA sample, and review '
                         'interpreter and language-line handoffs for the Others queue during the next campaign.'},
 'heatmap': {'description': 'This heat map shows the % of callers rating each survey question 1–2, by week (Monday '
                            'start). Darker red means more negative ratings. The number of responses per week is shown '
                            'under each week.',
             'insight': 'Negative Answer Satisfaction **rose from 15.4% and 15.0% in the first two weeks to 21.8% in '
                        'the week of Nov 17, and 23–25% in December**. Overall dissatisfaction peaked at **16.9% in '
                        'the week of Dec 1** (n = 59). Wait Time negatives were highest in week one (11.1%) and again '
                        'in December (11.8%, 12.5%). Agent Customer Service stayed at **7% or less every week**.',
             'interpretation': 'The problem is concentrated in answer quality and **got worse as the campaign went '
                               'on**, while agent behaviour stayed consistently good. Later weeks have smaller '
                               'samples, but the direction holds across four consecutive weeks with 50 or more '
                               'responses each (Nov 17 to Dec 8).',
             'recommendation': 'Add **answer quality as a standing item in the weekly team huddle**. When a question '
                               'passes **20% negative in a week with at least 50 responses** (as Answer did in the '
                               'weeks of Nov 17, Dec 1 and Dec 8), trigger a call-review session that same week. Also '
                               'check whether a new or seasonal call topic appeared in late November that agents were '
                               'not prepared for.',
             'conclusion': 'The weekly problem map shows that negative Answer Satisfaction ratings rose from about '
                           '**15% in the first two weeks to 21.8% in the week of November 17 and 23–25% in December**, '
                           'while negative ratings for Agent Customer Service stayed at **7% or below** every week. It '
                           'can be concluded that the decline in answer quality worsened as the campaign progressed '
                           'and was not caused by agent behaviour. The direction is consistent across four consecutive '
                           'weeks with at least 50 responses each.',
             'recommend': 'It is recommended that answer quality become a standing item in the weekly team huddle, and '
                          'that a call-review session be triggered whenever any service area exceeds 20% negative '
                          'ratings in a week with at least 50 responses.'},
 'exceptions': {'description': 'This detailed table has one row per day that had at least 15 responses. It shows that '
                               "day's KPIs and a status flag with the reason: **✖ Critical** (CSAT < 70% or Answer < "
                               '55%), **▲ Warning** (CSAT < 80%, Answer < 60% or Wait OK < 75%) or **✔ OK**. The '
                               "response bar shows each day's volume.",
                'insight': 'Of 15 rated days, **10 are OK, 4 are Warning and 1 is Critical**. The Critical day is '
                           '**Tuesday Nov 18** (CSAT 66.7%, Answer 45.8%, Wait 70.8%, n = 24). The Warning days are '
                           '**Wednesday Nov 5, the campaign launch** (CSAT 77.2%, Answer 58.4%, Wait 70.3%, the lowest '
                           'wait score of any rated day), and **Nov 16, 17 and 19**. The other 29 days had too few '
                           "responses to rate. **None of the 15 days fall outside their control limits** (Nov 18's "
                           'lower limit is 58.4%).',
                'interpretation': 'Problems clustered at two moments: **campaign launch** (wait-time pressure) and the '
                                  '**Nov 16–19 run**, when both answer quality and wait time fell. This tells '
                                  "supervisors exactly which dates' schedules and call recordings to pull. The Control "
                                  'check column shows these days breach business thresholds without being '
                                  'statistically unusual, so each flag is a prompt for a call review, not proof of a '
                                  'breakdown.',
                'recommendation': 'For every Warning or Critical day, the duty supervisor records a **short cause note '
                                  'within 24 hours** (staffing gap, system issue, unusual call topic). Compare actual '
                                  'staffing around Nov 5 and Nov 16–19 against forecast. Use this report as the '
                                  '**standing agenda for the morning huddle**.',
                'conclusion': 'The exceptions report shows that, of 15 rated days, **10 were OK, 4 were flagged as '
                              'Warning and 1 as Critical**: Tuesday, November 18, with CSAT of 66.7%, Answer '
                              'Satisfaction of 45.8% and Wait Time OK of 70.8%. The flagged days cluster around the '
                              'campaign launch on November 5, which had the lowest wait-time score, and the November '
                              '16–19 run. **None of these days fell outside its statistical control limits.** It can '
                              'be concluded that these days breached the business thresholds without being '
                              'statistically unusual, so they warrant call review but do not prove a service '
                              'breakdown.',
                'recommend': 'It is recommended that the duty supervisor record a short cause note within 24 hours for '
                             'every Warning or Critical day, that staffing on November 5 and November 16–19 be '
                             'compared against the forecast, and that this report serve as the standing agenda for the '
                             'morning huddle.'},
 'followup': {'description': 'This transaction-level table lists the 15 most recent low-score responses (Overall 1–2 '
                             'or NPS 0–6). Each row shows the five ratings (1–2 shaded red, 3 grey), the NPS, the '
                             'weakest service driver and a priority: **High** = Overall 1 or NPS 0–3, **Medium** = all '
                             'other low-score responses.',
              'insight': '**233 responses (18.9% of the campaign) qualify for follow-up, and 139 are High priority.** '
                         'In the latest 15, Answer Satisfaction is the weakest (or tied-weakest) area in **11**. The '
                         'log also exposes contradictory answers: **40 responses rate Overall 1–2 but give NPS 9–10**, '
                         'and 10 rate every question 4–5 but give NPS 0–6.',
              'interpretation': 'This is the *transactions* view a supervisor works from. In live operations, each '
                                'response would link back to its call record so the call can be reviewed and the '
                                'caller contacted (the public data has personal details removed). The contradictory '
                                'scores suggest some callers misread the 1–5 scale, so those rows need a quick check '
                                'before anyone coaches an agent on them.',
              'recommendation': 'Work the **High-priority list first, reviewing each call within 48 hours**, and tag '
                                'every reviewed call with a root cause (answer content, wait, agent behaviour, '
                                "transfer). Next campaign's dashboard can then show causes, not just scores. Send the "
                                'contradictory responses to the survey design team (for example, label the ends of '
                                'each scale more clearly) rather than treating them as agent performance issues.',
              'conclusion': 'The follow-up log shows that **233 responses (18.9% of the campaign)** qualified for '
                            'follow-up, of which **139 were High priority**. Answer Satisfaction was the weakest area '
                            'in 11 of the 15 most recent cases. The log also revealed contradictory responses: 40 '
                            'callers rated Overall Satisfaction 1–2 but gave an NPS of 9–10, and 10 rated every '
                            'question 4–5 but gave an NPS of 6 or below. It can be concluded that a substantial number '
                            'of callers need follow-up, mostly over answer quality, and that some responses likely '
                            'reflect confusion over the rating scale rather than actual service failures.',
              'recommend': 'It is recommended that QA leads review all High-priority calls within 48 hours and tag '
                           'each with a root cause (answer content, wait, agent behaviour or transfer), and that '
                           'contradictory responses be referred to the survey design team instead of being used in '
                           'agent coaching.'},
 'pacing': {'description': 'This chart tracks cumulative CSAT by day of campaign for the selected campaign and the '
                           'same campaign one year earlier, against the 80% target. Each point is CSAT across all '
                           'responses received up to that day, so the line settles as responses accumulate.',
            'insight': '2025 Campaign 5 opened at **77.2%** on launch day, recovered to **83.4% by day 7**, and '
                       'finished at **81.9%**. At day 31 it stood at 81.8%, about **1.2 points behind 2024 Campaign '
                       '5** (83.0% at the same point). Both campaigns stayed above target after the first week.',
            'interpretation': 'Comparing with the same campaign last year controls for season and survey cycle, so '
                              'supervisors can tell early whether a campaign is tracking better or worse. This '
                              'campaign is on target but slightly behind last year, which matches the slip in Answer '
                              'Satisfaction.',
            'recommendation': 'Check pacing on day 7 and day 14 of every campaign. If cumulative CSAT is more than 2 '
                              'points behind the same campaign last year by day 14, start call reviews early instead '
                              'of waiting for the campaign to end.',
            'conclusion': 'The pacing chart shows that 2025 Campaign 5 opened at **77.2%** on launch day, recovered to '
                          '**83.4% by day 7**, and finished at **81.9%**. At day 31 it stood **1.2 points behind 2024 '
                          'Campaign 5** (81.8% versus 83.0%), although both campaigns remained above target after the '
                          'first week. It can be concluded that the campaign stayed on target but tracked slightly '
                          'below the previous year, which is consistent with the decline in Answer Satisfaction.',
            'recommend': 'It is recommended that supervisors check campaign pacing on days 7 and 14, and that call '
                         'reviews begin early whenever cumulative CSAT trails the same campaign of the previous year '
                         'by more than 2 points at day 14.'}}

# Middle level: written for the full 2020–2025 range
MIDDLE = {'kpi': {'description': 'Four KPIs head the page. **Surveys analysed** is the number of survey responses. **CSAT (% '
                        'favorable)** is the share answering Agree or Strongly Agree to the overall satisfaction '
                        'question. **Net Promoter Score (NPS)** is the percentage of promoters (9–10) minus the '
                        'percentage of detractors (0–6) on the 0–10 recommendation question. **% Unfavorable** is the '
                        'share answering Disagree or Strongly Disagree to overall satisfaction.',
         'insight': '**80.9%** of callers were satisfied, and an NPS of **+53** shows promoters clearly outnumber '
                    'detractors. Quarterly CSAT has stayed within about 77–84% for five years. The **12.8%** '
                    'unfavorable rate is steady across campaigns, which points to a recurring issue rather than a '
                    'one-time problem. Answer satisfaction is the weakest driver at **66.3%** favorable, so better '
                    'issue resolution offers the biggest gain.',
         'interpretation': 'The call center serves most callers well but has stopped improving. Across **28,790** '
                           'surveys, 80.9% of callers were satisfied and promoters clearly outnumber detractors, so '
                           'the service is solid and reliable. The remaining 12.8% were unfavorable, and that share '
                           'has held steady across campaigns and years, so it looks like a recurring problem rather '
                           'than a passing one. Results are consistent but flat, so the next gains must come from '
                           "targeted improvement, especially in how well callers' issues are resolved.",
         'recommendation': 'Maintain current service levels, set a target (for example, CSAT above 85%), and direct '
                           'training and process improvements at answer quality and first-call resolution.',
         'conclusion': 'Across **28,790 surveys** from 2020 to 2025, **80.9%** of callers were satisfied, and the NPS '
                       'of **+53** shows that promoters clearly outnumber detractors. However, **12.8%** of callers '
                       'remained unfavorable, a share that has stayed steady across campaigns, and Answer Satisfaction '
                       'was the weakest driver at **66.3%**. It can be concluded that the call center delivers a solid '
                       'and consistent service but has not improved over the period, and that further gains depend on '
                       'better issue resolution.',
         'recommend': 'It is recommended that management maintain current service levels while setting an improvement '
                      'target, such as CSAT above 85%, and direct training and process improvements toward answer '
                      'quality and first-call resolution.'},
 'trend': {'description': 'Two line charts share one quarter axis, from 2020Q4 to 2025Q4: CSAT (% favorable) on top '
                          'and NPS below. Quarters with fewer than 200 responses are hidden. Each chart has its own '
                          'scale, and a dotted linear trend line with a significance test is drawn on each.',
           'insight': 'CSAT is flat. It stays within about 77–84% over the five years, with no clear upward or '
                      'downward trend. The low points are 2021Q3 (76.9%) and 2023Q1 (76.8%), when NPS also fell to '
                      'about 45. The high points are 2024Q1 (84.4% CSAT) and 2023Q2 (NPS about 62). NPS swings more '
                      'than CSAT, moving between roughly 45 and 62 and often jumping several points from one quarter '
                      'to the next. The two lines usually move together: the 2023Q1 dip and the 2023Q2 rebound show up '
                      'in both. The trend test confirms it: **CSAT is statistically flat (+0.10 points a quarter, p = '
                      '0.24)**, while **NPS has a small but significant upward trend (+0.39 points a quarter, about '
                      '+1.6 a year, p = 0.02)**.',
           'interpretation': 'Service quality has been consistent but has not improved. The 2023Q1 dip and quick '
                             'recovery look like a short disruption, such as a staffing or process issue, rather than '
                             'a lasting decline. Quarter-to-quarter NPS moves should be read with caution, since small '
                             'changes can be random. The recent quarters (2024Q2 to 2025Q4) hold steady at about '
                             '80–83% CSAT, so there is no sign of a recent decline. Willingness to recommend is edging '
                             'up even though the share of satisfied callers is not; the gain is small, so confirm it '
                             'over the next few quarters.',
           'recommendation': 'Investigate 2023Q1: find out what happened (staffing, volume, policy changes) and put '
                             'safeguards in place so it does not recur. Set a target, for example CSAT above 85%, to '
                             'move beyond the 77–84% range. Treat CSAT moves of about 4 points or less as normal '
                             'variation and flag only larger drops. Since overall results are flat, target the weakest '
                             'driver (answer satisfaction) to lift CSAT.',
           'conclusion': 'The quarterly trend shows that CSAT remained within **77–84%** over five years, with low '
                         'points in 2021Q3 (76.9%) and 2023Q1 (76.8%) and a high of 84.4% in 2024Q1. The trend test '
                         'confirms that **CSAT is statistically flat** (+0.10 points per quarter, p = 0.24), whereas '
                         '**NPS shows a small but significant upward trend** (+0.39 points per quarter, p = 0.02). It '
                         'can be concluded that service quality has been consistent but has not improved, that the '
                         '2023Q1 dip was a short-lived disruption, and that willingness to recommend is rising slowly '
                         'even though satisfaction is not.',
           'recommend': 'It is recommended that management investigate the causes of the 2023Q1 dip to prevent a '
                        'recurrence, set a target above the historical range (for example, CSAT above 85%), treat '
                        'quarterly CSAT changes of about 4 points or less as normal variation, and confirm the NPS '
                        'improvement over the next few quarters.'},
 'departments': {'description': 'This heat map compares the five language groups with at least 100 responses (the '
                                'closest thing to departments in this data) across six KPIs, with the all-caller '
                                "average in the top row. Each cell shows the group's value; color shows how far it "
                                'sits above (blue) or below (red) the all-caller average for that KPI.',
                 'insight': '**Spanish is the best group on all six KPIs**: CSAT 86.5%, Wait 88.2%, Agent Service '
                            '91.3%, Job Knowledge 89.5%, Answer 77.0% and NPS +73.7. **English (81% of all surveys) is '
                            'slightly below average on all six**, so it sets the overall numbers. **Russian has one '
                            'sharp problem**: Answer Satisfaction of 42.9%, 23 points below average, while its CSAT, '
                            'Wait and Job Knowledge ratings are above average. Both Chinese groups score well on '
                            'satisfaction (about 85% CSAT) but have the **lowest NPS** (+42.2 and +48.4).',
                 'interpretation': 'Performance differs far more by language group than by campaign. Spanish shows the '
                                   'same system can deliver much better results. Russian and the Chinese groups each '
                                   'have one specific gap rather than general weakness, so they need targeted fixes '
                                   'rather than general training.',
                 'recommendation': 'Use Spanish-team practices as the internal benchmark. Review Russian answer '
                                   'quality (interpreters, translated scripts, accuracy of information), investigate '
                                   'why Chinese callers rarely recommend 311 despite being satisfied, and set '
                                   'group-level targets so each language team owns its KPIs.',
                 'conclusion': 'The department heat map shows that the **Spanish group performed best on all six '
                               'KPIs**, including CSAT of 86.5%, Answer Satisfaction of 77.0% and NPS of +73.7. The '
                               'English group, which accounts for 81% of surveys, was **slightly below average on all '
                               'six measures**. The Russian group had a single sharp weakness, **Answer Satisfaction '
                               'of 42.9%** (23 points below average), and both Chinese groups combined high '
                               'satisfaction (about 85% CSAT) with the **lowest NPS** (+42.2 and +48.4). It can be '
                               'concluded that performance varies more by language group than by campaign, and that '
                               'the weaker groups each have a specific gap rather than a general weakness.',
                 'recommend': 'It is recommended that Spanish-team practices be used as the internal benchmark, that '
                              'Russian-language answer quality be reviewed (interpreters, translated scripts and '
                              'accuracy of information), that the low recommendation rate among Chinese callers be '
                              'investigated, and that group-level targets be set so each language team is accountable '
                              'for its own KPIs.'},
 'campaigns': {'description': 'A 100% stacked horizontal bar chart shows how the five overall satisfaction responses '
                              'split within each survey campaign (Pilot, then Campaigns 1 to 5). Each bar adds up to '
                              "100% of that campaign's responses. Colors run from red (Strongly Disagree) through grey "
                              '(Neutral) to dark blue (Strongly Agree). Labels appear only on segments of 8% or more; '
                              'hover for the rest.',
               'insight': 'The campaigns look almost identical. Strongly Agree is 53–57% of responses in every '
                          'campaign and Agree 24–28%, so favorable responses land at about 80–82% across the board. '
                          'Campaign 4 is the highest at about 82%, and Campaign 3 is the lowest at 79.7%. Strongly '
                          'Disagree holds steady at 8–10%, and Neutral is no more than about 7% in any campaign. The '
                          'Pilot has the smallest Strongly Agree share (53%) but the largest Agree share (28%), so its '
                          'favorable rate matches the others.',
               'interpretation': 'Satisfaction did not change noticeably from one campaign to the next, so no campaign '
                                 'stands out as clearly better or worse. Callers tend to feel strongly, either very '
                                 'satisfied or very dissatisfied, and few sit in the middle. The unfavorable group '
                                 '(about 13%) has not shrunk since the Pilot, which suggests a lasting issue in '
                                 'service delivery rather than a problem tied to one campaign.',
               'recommendation': 'Treat the dissatisfied group as one ongoing problem and analyse it across all '
                                 'campaigns. Start by finding what drives Strongly Disagree responses, especially '
                                 'answer satisfaction and job knowledge ratings, together with call types. Campaign 4 '
                                 'has the highest favorable share and the lowest Strongly Disagree share, so check '
                                 'whether anything in its approach can be repeated. Test any future change against the '
                                 '80–82% favorable baseline.',
               'conclusion': 'The campaign comparison shows that the satisfaction mix was nearly identical across the '
                             'Pilot and Campaigns 1 to 5: Strongly Agree ranged from **53% to 57%**, favorable '
                             'responses from about **80% to 82%**, and Strongly Disagree from 8% to 10%. Campaign 4 '
                             'had the highest favorable share (about 82%) and Campaign 3 the lowest (79.7%). It can be '
                             'concluded that no campaign performed meaningfully better or worse than the others, and '
                             'that the dissatisfied group of about 13% is a persistent problem rather than one tied to '
                             'a particular campaign.',
               'recommend': 'It is recommended that the dissatisfied group be treated as one ongoing problem and '
                            'analysed across all campaigns, starting with its answer-satisfaction and job-knowledge '
                            'ratings, and that any future process change be evaluated against the 80–82% favorable '
                            'baseline.'},
 'languages': {'description': 'A bubble chart compares language groups with at least 100 responses. The x-axis is % '
                              'favorable on answer satisfaction and the y-axis is % favorable on overall satisfaction. '
                              "Bubble size is survey volume, color is the group's NPS (darker = higher), and the "
                              'dashed line is a trend line fitted through the groups.',
               'insight': 'Spanish speakers are the happiest group: about 86% overall, 77% on answer satisfaction and '
                          'the highest NPS (+74). English speakers are the largest group (23,189 surveys) and the '
                          'least satisfied overall at about 80%, with answer satisfaction of about 64%. Russian '
                          'speakers are the clear outlier, with only about 43% favorable on answer satisfaction, even '
                          'though their overall satisfaction (about 82%) is not low. The two Chinese groups are '
                          'similar (about 85% overall, 76% answer) but have a low NPS of about 42–48.',
               'interpretation': 'Answer and overall satisfaction tend to move together, but not perfectly. The '
                                 'Russian group shows callers can be fairly satisfied overall while unhappy with the '
                                 'answers, which may point to language or interpretation barriers. The Chinese groups '
                                 'show the opposite problem: good satisfaction but low willingness to recommend. '
                                 'English speakers dominate the volume, so they set the overall KPIs. Two cautions: '
                                 'the y-axis is zoomed in, so gaps look larger than they are, and the groups other '
                                 'than English and Spanish have fewer than 500 surveys each. The trend line rests on '
                                 'only five points, so do not read it as a firm relationship.',
               'recommendation': 'Review Russian-language service first: interpreter quality, translated scripts and '
                                 'the accuracy of information given. Investigate why the Chinese groups have a low NPS '
                                 'despite good satisfaction, for example through follow-up questions. Study '
                                 'Spanish-language service for practices other groups can use. Improving '
                                 'English-language answer quality would raise overall CSAT the most. Collect more '
                                 'responses from smaller language groups to make future comparisons more reliable.',
               'conclusion': 'The segment scatter shows that answer and overall satisfaction generally move together '
                             'across language groups. Spanish speakers were the most satisfied (about 86% overall and '
                             '77% on answers), while English speakers, the largest group with 23,189 surveys, were the '
                             'least satisfied overall at about 80%. Russian speakers were the clear outlier, with only '
                             '**about 43% favorable on answers** despite about 82% overall satisfaction. It can be '
                             'concluded that language-related barriers may affect the quality of answers for some '
                             "groups, and that English-language service determines the organization's overall results "
                             'because of its volume.',
               'recommend': 'It is recommended that Russian-language service be reviewed first, that Spanish-language '
                            'practices be studied for transfer to other groups, that English-language answer quality '
                            'be improved to lift overall CSAT, and that more responses be collected from smaller '
                            'language groups to make future comparisons more reliable.'},
 'matrix': {'description': 'A scatter plot (each point labelled with its % favorable) places each of the four service '
                           'drivers by performance (x-axis: % favorable, 2020–2025) and impact (y-axis: the '
                           "correlation of that driver's rating with Overall Satisfaction). Dashed lines at the four "
                           "drivers' averages split the chart into quadrants: **Fix first** (high impact, low "
                           'performance), **Protect** (high impact, high performance), **Maintain** and **Monitor**.',
            'insight': '**Answer Satisfaction is alone in the Fix-first quadrant**: the lowest performance (66.3% '
                       'favorable) with high impact (r = 0.69). **Agent Job Knowledge has the highest impact (r = '
                       '0.73)** and good performance (84.2%), so it is the strength to protect. Agent Customer Service '
                       'performs best (89.5%) with about average impact (r = 0.67), and Wait Time has the weakest link '
                       'to satisfaction (r = 0.62).',
            'interpretation': 'The matrix turns a ranking of drivers into a priority list. Improving answer quality '
                              'offers the largest return, because it is both weak and closely tied to overall '
                              'satisfaction. Job knowledge matters even more, so cutting training would put the '
                              'strongest driver at risk. Correlation shows association, not cause, but the pattern '
                              'agrees with the decision tree below, where Answer Satisfaction is the second most '
                              'important factor.',
            'recommendation': "Put answer quality and first-call resolution first in next quarter's plan, protect "
                              'job-knowledge training, and hold wait-time investment at current levels rather than '
                              'increasing it, since wait time has the weakest link to satisfaction.',
            'conclusion': 'The fix-first matrix shows that **Answer Satisfaction is the only driver with both low '
                          'performance (66.3% favorable) and high impact** on overall satisfaction (r = 0.69). Agent '
                          'Job Knowledge has the **highest impact** (r = 0.73) and good performance (84.2%), while '
                          'Wait Time has the weakest association with satisfaction (r = 0.62). It can be concluded '
                          'that improving answer quality offers the greatest potential return, and that job knowledge '
                          'is a key strength that must be protected.',
            'recommend': 'It is recommended that answer quality and first-call resolution be given top priority in the '
                         "next quarter's plan, that job-knowledge training be maintained, and that wait-time "
                         'investment be held at current levels rather than increased.'},
 'tree': {'description': 'A feature-importance bar chart sits beside a three-level decision tree that classifies '
                         'callers into NPS groups (Detractor 0–6, Passive 7–8, Promoter 9–10) from their five ratings '
                         'and the survey turnaround time. Each tree node shows its split, its share of callers and its '
                         'NPS mix.',
          'insight': "Overall Satisfaction carries **87.7%** of the model's importance, followed distantly by Answer "
                     'Satisfaction at **10.0%** and Agent Customer Service at 2.3%. Turnaround, Wait Time and Job '
                     'Knowledge carry essentially **0%**. The tree shows a hard threshold: when both Overall and '
                     'Answer Satisfaction are 3 or lower (≤ 3.5), a segment of **16.6%** of callers lands in the '
                     'Detractor zone.',
          'interpretation': 'NPS is gated by getting a satisfactory answer. Backend timing, such as how long the '
                            'survey took to complete, has virtually no influence on whether a caller recommends 311.',
          'recommendation': "Don't spend improvement effort on shorter turnaround, since it does not move NPS. Build "
                            'team standards and coaching around the threshold instead: flag every interaction with '
                            'Answer Satisfaction of 3 or lower for QA review, so fewer callers leave with an answer '
                            'rated below 4.',
          'conclusion': 'The decision tree and feature importance show that **Overall Satisfaction accounts for '
                        "87.7%** of the model's decisions, followed by **Answer Satisfaction at 10.0%** and Agent "
                        'Customer Service at 2.3%, while turnaround time, wait time and job knowledge contribute '
                        'almost nothing. When both Overall and Answer Satisfaction are rated 3 or lower, a segment of '
                        '**16.6% of callers** falls into the Detractor group. It can be concluded that a satisfactory '
                        'answer is the gateway to a positive NPS, and that backend timing has virtually no influence '
                        'on whether callers recommend 311.',
          'recommend': 'It is recommended that improvement effort not be directed at shortening turnaround time, and '
                       'that team standards and coaching instead be built around the answer-quality threshold, with '
                       'every interaction rated 3 or lower on Answer Satisfaction flagged for QA review.'},
 'volume': {'description': 'This month-by-year heat map shows how many survey responses arrived each month; each cell '
                           "gives the count and its share of that year's responses.",
            'insight': 'Survey capture grew from **1,004** records in 2020 to a peak of **6,465** in 2024 (6,025 in '
                       '2025). After irregular scheduling in 2020 and 2021, collection settled by 2023 into five '
                       'concentrated anchor months: January, May, July, September and November. Peak months hold about '
                       '1,000–1,200 responses, while off-months drop to near zero.',
            'interpretation': 'The uneven monthly pattern is not a data gap but a deliberate design. NYC Local Law 26 '
                              'of 2021 requires NYC311 to run at least five customer-satisfaction survey campaigns a '
                              'year. Invitations go out in bursts during launch months, with small spillover into the '
                              'following month.',
            'recommendation': 'Plan QA reviews and reporting around the five campaign months, and compare performance '
                              'campaign over campaign (for example, the May cohort against the July cohort) rather '
                              'than month over month, since off-months lack enough responses to be meaningful.',
            'conclusion': 'The monthly heat map shows that survey responses grew from **1,004 in 2020 to a peak of '
                          '6,465 in 2024**, and that by 2023 collection had settled into five concentrated months: '
                          'January, May, July, September and November. Peak months hold about 1,000–1,200 responses, '
                          'while other months have almost none. It can be concluded that this uneven pattern is a '
                          'deliberate campaign design, consistent with NYC Local Law 26 of 2021, which requires at '
                          'least five survey campaigns a year, rather than a gap in the data.',
            'recommend': 'It is recommended that QA reviews and reporting be planned around the five campaign months, '
                         'and that performance be compared campaign over campaign rather than month over month, since '
                         'off-months lack enough responses to be meaningful.'}}

# Top level: written for the full 2020–2025 range (latest year 2025)
TOP = {'summary': {'description': 'Four headline indicators summarise the latest full year (2025), each with its change from '
                            '2024, and the 2025 split of promoters, passives and detractors.',
             'insight': 'In 2025, **CSAT was 80.9% (−1.2 points)**, **NPS +54.7 (+0.5)**, **Answer Satisfaction 66.6% '
                        '(−0.9)** and respondents **6,025 (−440)**. Promoters made up **70.7%** of callers and '
                        'detractors **16.0%**.',
             'interpretation': 'Results moved only modestly: satisfaction and answer quality slipped about a point '
                               'while loyalty edged up. Seven in ten callers are promoters, so the base of goodwill is '
                               'strong. The strategic question is how to convert the remaining three in ten.',
             'recommendation': 'Lead executive reporting with NPS and Answer Satisfaction together: NPS measures '
                               'loyalty, and Answer Satisfaction is the main lever for improving it.',
             'conclusion': 'The summary indicators show that in 2025 CSAT was **80.9%** (down 1.2 points from 2024), '
                           'NPS was **+54.7** (up 0.5), Answer Satisfaction was **66.6%** (down 0.9), and **6,025** '
                           'callers responded. Promoters made up **70.7%** of callers and detractors **16.0%**. It can '
                           'be concluded that results moved only modestly during the year and that the organization '
                           'holds a strong base of goodwill; the main strategic question is how to convert the '
                           'remaining three in ten callers.',
             'recommend': 'It is recommended that executive reporting lead with NPS and Answer Satisfaction together, '
                          'since NPS measures loyalty and Answer Satisfaction is the main lever for improving it.'},
 'scorecard': {'description': 'A strategic scorecard lists five executive KPIs with the latest full year (2025), the '
                              'change from 2024, the target, a status flag and a sparkline from 2020 to 2025. Targets '
                              'for CSAT (85%) and Answer Satisfaction (75%) come from the middle-level '
                              'recommendations, and the Answer 1/5 KPI comes from the top-level recommendation to '
                              'eliminate those interactions. The NPS (60) and % Unfavorable (10%) targets are '
                              'illustrative.',
               'insight': '**All four targeted KPIs are off target in 2025.** CSAT is 80.9% (down 1.2 points from '
                          '2024, 4.1 points short), NPS is +54.7 (up 0.5, 5.3 points short), Answer Satisfaction is '
                          '66.6% (down 0.9, 8.4 points short) and % Unfavorable is 12.7% (up 1.0, 2.7 points over). '
                          'The one KPI moving the right way is the share of callers rating the answer 1/5, which fell '
                          'slightly to 11.8%.',
               'interpretation': 'The organization is meeting a stable service baseline but not its improvement goals. '
                                 '2024 was the best year on most KPIs, and 2025 gave some of that back. The gap is '
                                 'largest on answer quality, the same weakness every other level of the dashboard '
                                 "points to, so it is the strategic priority rather than one team's problem.",
               'recommendation': 'Adopt these KPIs and targets formally and review the scorecard every campaign. Make '
                                 'the Answer Satisfaction gap (8.4 points) the headline goal for 2026, funded through '
                                 'first-contact resolution and knowledge-base work, and report the Answer 1/5 share '
                                 'alongside it as the leading indicator.',
               'conclusion': 'The strategic scorecard shows that **all four targeted KPIs were off target in 2025**: '
                             'CSAT was 4.1 points below its 85% target, NPS 5.3 points below 60, Answer Satisfaction '
                             '**8.4 points below 75%**, and the unfavorable share 2.7 points above its 10% ceiling. '
                             'Only the share of callers rating the answer 1/5 moved in the right direction, falling '
                             'slightly to 11.8%. It can be concluded that the organization is maintaining a stable '
                             'service baseline but is not meeting its improvement goals, with the largest gap in '
                             'answer quality.',
               'recommend': 'It is recommended that leadership formally adopt these KPIs and targets, review the '
                            'scorecard after every campaign, and make closing the 8.4-point Answer Satisfaction gap '
                            'the headline goal for 2026, supported by first-contact resolution and knowledge-base '
                            'initiatives.'},
 'growth': {'description': 'These bar charts show CSAT and NPS for each year from 2020 (the pilot) to 2025. Each bar '
                           'is labelled with its change from the previous year, the satisfaction equivalent of a '
                           'yearly growth rate.',
            'insight': '**NPS grew every year from 2020 to 2023** (+4.5, +3.9 and +1.2 points), from +45.0 to +54.7, '
                       '**then levelled off** (−0.4 in 2024, +0.5 in 2025). **CSAT shows no growth**: it alternates '
                       'between gains and losses of 1–2 points, staying at 79–82%.',
            'interpretation': 'Loyalty improved in the early years and has now plateaued, while satisfaction never '
                              'grew. Without a new improvement program, the coming years will likely look like 2024 '
                              'and 2025.',
            'recommendation': 'Set a yearly growth goal (for example, +2 NPS points and +1 CSAT point a year) and '
                              'track it on this chart. The forecast below shows what happens if the plateau continues.',
            'conclusion': 'The year-over-year growth chart shows that **NPS rose every year from 2020 to 2023** (+4.5, '
                          '+3.9 and +1.2 points), from +45.0 to +54.7, before **levelling off** in 2024 (−0.4) and '
                          '2025 (+0.5). CSAT, in contrast, alternated between gains and losses of 1–2 points and '
                          'stayed between 79% and 82%. It can be concluded that loyalty improved in the early years '
                          'but has now plateaued, and that satisfaction has not grown over the period.',
            'recommend': 'It is recommended that leadership set a yearly growth goal, such as +2 NPS points and +1 '
                         'CSAT point per year, and track progress against it on this chart.'},
 'forecast': {'description': 'The chart plots campaign-level CSAT and NPS for all 26 campaigns (2020–2025), each '
                             "plotted at its campaign's midpoint, with a linear-trend forecast (dashed) for the five "
                             'expected 2026 campaigns and a 95% prediction interval (grey band): the range a single '
                             'campaign is likely to fall in. Dotted lines mark the targets.',
              'insight': '**CSAT is forecast at about 81.6% for every 2026 campaign (95% range 77–86%)**; its trend is '
                         'not significant (+0.31 points a year, p = 0.25). **NPS is forecast to rise from about 56 to '
                         '57 during 2026 (95% range 47–66)**, on a small but significant trend (+1.19 a year, p = '
                         '0.04). The 85% CSAT target sits at the top edge of the expected range.',
              'interpretation': 'If nothing changes, CSAT will stay where it has been for five years and will almost '
                                'never reach 85%. NPS is improving, but at the current pace it would reach the '
                                'illustrative target of 60 only around 2029. The forecast is a straight-line '
                                'projection of past campaigns: it shows where the current path leads, not what a new '
                                'program could achieve.',
              'recommendation': 'Treat the gap between the forecast and the target as the size of the change needed: '
                                'reaching 85% CSAT means lifting results by about 3–4 points beyond the trend, which '
                                'requires a deliberate program (answer quality, first-contact resolution) rather than '
                                'more of the same. Re-run the forecast after each 2026 campaign to see whether results '
                                'move above the forecast line.',
              'conclusion': 'The forecast projects CSAT at about **81.6% for each 2026 campaign** (95% range 77–86%), '
                            'based on a trend that is not statistically significant (+0.31 points per year, p = 0.25), '
                            'and **NPS rising from about 56 to 57** (95% range 47–66) on a small but significant trend '
                            '(+1.19 points per year, p = 0.04). It can be concluded that, if current conditions '
                            'continue, CSAT will rarely reach the 85% target and NPS will reach the target of 60 only '
                            'around 2029.',
              'recommend': 'It is recommended that leadership treat the gap between the forecast and the target, about '
                           '3–4 CSAT points, as the size of the change required; launch a deliberate improvement '
                           'program focused on answer quality and first-contact resolution; and re-run the forecast '
                           'after each 2026 campaign to check whether results rise above the projected line.'},
 'compliance': {'description': 'The chart compares the survey campaigns run each year against the minimum of five set '
                               'by NYC Local Law 26 of 2021, next to total survey responses per year.',
                'insight': 'NYC311 ran **five campaigns in every year from 2021 to 2025**, meeting the legal minimum '
                           'each year (2020 was a single pilot). Responses grew from **1,004** in the pilot year to a '
                           'peak of **6,465** in 2024 (6,025 in 2025). The month-by-month view shows the five anchor '
                           'months the schedule settled into by 2023: January, May, July, September and November.',
                'interpretation': "The organization is meeting its survey mandate. Each year's KPIs rest on "
                                  '5,400–6,500 responses, so year-level results are precise to about ±1 point and safe '
                                  'to compare.',
                'recommendation': 'Keep the five-campaign schedule in the same months so year-over-year comparisons '
                                  'stay like-for-like, and report mandate compliance alongside the KPIs in executive '
                                  'reviews.',
                'conclusion': 'The compliance chart shows that NYC311 ran **five survey campaigns in every year from '
                              '2021 to 2025**, meeting the minimum required by NYC Local Law 26 of 2021, and that '
                              'responses grew from 1,004 in the 2020 pilot to 6,025 in 2025. It can be concluded that '
                              "the organization is meeting its survey mandate and that each year's KPIs rest on enough "
                              'responses (5,400–6,500) to be precise to about ±1 point.',
                'recommend': 'It is recommended that the five-campaign schedule be kept in the same months so that '
                             'year-over-year comparisons remain like-for-like, and that mandate compliance be reported '
                             'alongside the KPIs in executive reviews.'},
 'apriori': {'description': 'These summary cards come from target-oriented association rule mining (Apriori, minimum '
                            'support 5%, minimum confidence 30%). It maps combinations of caller ratings to the NPS '
                            'segment they predict, shown as Reliability (confidence), Customer Share (support) and '
                            'Impact (lift: how many times more likely than average).',
             'insight': 'A perfect 5/5 across all five questions predicts a Promoter with **97.6%** reliability and '
                        'covers **28.9%** of callers. At the other end, Answer Satisfaction of 1/5 is the most severe '
                        'pain point: it predicts a Detractor with **66.4%** reliability, **4.04×** more likely than '
                        'average.',
             'interpretation': 'Answer quality anchors customer sentiment. Even when agents are polite and waits are '
                               'short, an unsatisfactory answer will very likely turn the caller into a Detractor. '
                               'Passives are a conversion opportunity: they often rate overall satisfaction 4/5 but '
                               'are held back by average job knowledge or wait time.',
             'recommendation': 'Shift strategic budget from general customer-service etiquette training to '
                               'first-contact resolution and technical job-knowledge programs. Set a top-level KPI to '
                               'eliminate 1/5 Answer Satisfaction interactions.',
             'conclusion': 'The association rules show that a perfect 5/5 rating on all five questions predicts a '
                           'Promoter with **97.6% reliability** and covers **28.9% of callers**, while an Answer '
                           'Satisfaction rating of 1/5 predicts a Detractor with **66.4% reliability, 4.04 times more '
                           'likely** than average. Passives typically rate overall satisfaction 4/5 but are held back '
                           'by average job knowledge or wait time. It can be concluded that answer quality anchors '
                           'customer sentiment, that an unsatisfactory answer is the most serious risk to NPS, and '
                           'that passives represent the clearest opportunity for conversion.',
             'recommend': 'It is recommended that strategic budget shift from general customer-service etiquette '
                          'training toward first-contact resolution and technical job-knowledge programs, and that '
                          'leadership adopt a KPI to eliminate interactions rated 1/5 on Answer Satisfaction.'}}

# Page-level conclusion and numbered recommendations (recommendation, owner)
PAGE_CONCLUSIONS = {'LOWER': ('Overall, the operational analysis of 2025 Campaign 5 concludes that the call center met its satisfaction '
           'target and showed no statistically unusual days, but that answer quality is the consistent weakness across '
           'every view: it declined against the previous campaign, it was the lowest-rated driver in most low-score '
           'responses, and it worsened as the campaign progressed. The English queue, because of its volume, accounts '
           'for most dissatisfied callers, while the Spanish queue demonstrates that higher performance is achievable '
           'within the same system.',
           [('Adopt Answer Satisfaction as a daily KPI with a target of at least 70%.', 'Floor supervisors'),
            ('Review a weekly QA sample of calls rated 1–2 on Answer Satisfaction, update knowledge-base articles and '
             'scripts for recurring topics, and coach agents on explaining next steps.',
             'QA leads'),
            ('Pair English-queue agents with top Spanish-queue agents for peer learning, and place the English queue '
             'first in the QA sample.',
             'Team leads'),
            ('Escalate on a control-limit breach or two consecutive days below target, and record a cause note within '
             '24 hours for every flagged day.',
             'Duty supervisor'),
            ('Review High-priority low-score calls within 48 hours with root-cause tags, and refer contradictory '
             'responses to the survey design team.',
             'QA leads')]),
 'MIDDLE': ('Overall, the tactical analysis concludes that service quality has been stable but flat for five years, '
            'that performance differs more by language group than by campaign, and that answer quality is the factor '
            'with the greatest potential to raise both satisfaction and NPS, while job knowledge is the strength to '
            'protect and backend timing has little effect.',
            [("Make answer quality and first-call resolution the priority of next quarter's plan.",
              'Operations manager'),
             ('Use Spanish-team practices as the internal benchmark and set KPI targets for each language group.',
              'Operations manager'),
             ('Review Russian-language service, including interpreter quality and translated scripts.', 'QA manager'),
             ('Protect agent job-knowledge training, the driver most strongly linked to overall satisfaction.',
              'Training lead'),
             ('Monitor results by campaign and quarter, treating CSAT changes of about ±4 points as normal variation.',
              'QA manager')]),
 'TOP': ('Overall, the strategic analysis concludes that NYC311 is meeting its legal survey mandate and maintains a '
         'stable service baseline with a strong base of promoters, but it is not meeting its improvement targets: CSAT '
         'has not grown in five years, NPS growth has plateaued, and the forecast shows that the 85% CSAT target is '
         'out of reach without deliberate change. Answer quality is the common thread behind both the risks and the '
         'opportunities identified.',
         [('Formally adopt the scorecard KPIs and targets, and review them after every campaign.', 'Leadership'),
          ('Make closing the 8.4-point Answer Satisfaction gap the headline goal for 2026, funded through '
           'first-contact resolution and knowledge-base programs.',
           'Leadership'),
          ('Set yearly growth goals of about +2 NPS points and +1 CSAT point.', 'Leadership'),
          ('Keep the five-campaign survey schedule and report mandate compliance with the KPIs.', 'Performance office'),
          ('Shift budget from general etiquette training to first-contact resolution and job-knowledge programs, and '
           'track the share of answers rated 1/5 toward zero.',
           'Leadership')])}
