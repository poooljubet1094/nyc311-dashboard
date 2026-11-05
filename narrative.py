"""Written analysis for every visual (Description, Insight, Interpretation, Recommendation)."""

# Lower level: written for 2025 Campaign 5 (the latest campaign)
LOWER = {'kpi': {'description': 'Six KPI cards for 2025 Campaign 5, each showing the change against the previous campaign '
                        '(2025 Campaign 4): survey responses, CSAT, NPS, Wait Time OK, Answer Satisfaction and the '
                        'number of dissatisfied callers.',
         'insight': 'CSAT is **81.9%** (on target, **+0.3 pt**) and NPS is **+56.8** (flat, +0.1). Dissatisfied '
                    'callers fell from **161 to 139 (−22)**. Two KPIs moved the wrong way: **Answer Satisfaction '
                    'slipped from 68.7% to 66.6% (−2.1 pt)** and Wait Time OK slipped from 83.7% to 82.8% (−0.9 pt).',
         'interpretation': 'Overall service is stable and above target, so there is no emergency. But Answer '
                           'Satisfaction, the one KPI clearly getting worse, is a strong driver of overall '
                           'satisfaction (r = +0.69) and NPS (r = +0.64) in the correlation analysis. If it '
                           'keeps sliding, CSAT and NPS will follow.',
         'recommendation': 'Keep the current service approach, but make **Answer Satisfaction the focus KPI** for the '
                           'next campaign. Give it its own target (for example ≥ 70%) and review it in the daily team '
                           'huddle next to CSAT.'},
 'daily': {'description': "The top panel shows each day's CSAT as a dot (blue = on target, red = below target, grey = "
                          'fewer than 15 responses) and a 7-day rolling CSAT line against the 80% target. The bottom '
                          'panel shows how many survey responses arrived each day.',
           'insight': '**75% of all responses (924 of 1,235) arrived in the first 12 days** (Nov 5–16). The busiest '
                      'day was **Wednesday Nov 12, with 221 responses** and the most dissatisfied callers of any day '
                      "(25), and Wednesdays alone account for 30% of the campaign's feedback. Rolling CSAT held at "
                      '**82–84% until Nov 19**, then fell below target to a low of **73.9% (7 days to Nov 23)** and '
                      'again to **74.6% (Dec 4–7)**, before recovering to 89.3% by Dec 11. There were **four reliable '
                      'days in a row below target, Nov 16–19** (78.6%, 75.0%, 66.7%, 73.3%).',
           'interpretation': 'Feedback volume follows the survey send waves (large Wednesday bursts), so supervisors '
                             'can only confirm problems with confidence during the first two weeks. The mid-November '
                             'dip was a sustained run, not a one-off. Late-campaign single-day swings (for example 33% '
                             'on Dec 13) rest on two or three responses and should not trigger action by themselves.',
           'recommendation': 'Review this dashboard **every morning during the first two weeks** of each campaign, and '
                             'the day after each survey send. Treat **two consecutive reliable days below 80%** as an '
                             'escalation trigger: on that rule, Nov 16–17 would have prompted a review before the '
                             'Critical day on Nov 18. For later weeks, act on the rolling line, not on small single '
                             'days.'},
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
                            'it, how to track the request) when the answer cannot be what the caller hoped for.'},
 'queues': {'description': 'Grouped bars compare the four language queues (English, Spanish, Chinese, Others) on % '
                           'positive for CSAT, Wait Time, Agent Service and Answer Satisfaction, against the 80% '
                           'target. The table adds volume share, NPS and counts of dissatisfied callers and '
                           'detractors.',
            'insight': 'The **English queue handles 75.5% of responses** and is the **only queue below the CSAT target '
                       '(79.5%)**. It has the lowest Answer Satisfaction among the large queues (64.2%) and accounts '
                       'for **120 of the 139 dissatisfied callers (86%)**. **Spanish leads on every measure**: CSAT '
                       '90.8%, Answer 81.6%, NPS +78.6. Chinese is also strong (CSAT 89.1%, n = 64). The **Others '
                       'queue** (Russian, Korean, Arabic, Polish, French and other languages; n = 42) has the lowest '
                       'Answer Satisfaction, **35.7% (15 of 42)**, and the lowest Wait Time OK (76.2%), but the sample '
                       'is small.',
            'interpretation': 'Because English carries three-quarters of the volume, its small gap below target '
                              "produces most of the campaign's dissatisfaction. Lifting English answer satisfaction by "
                              'a few points would move the overall KPI more than anything else. The Spanish queue '
                              'works under the same system and still reaches 81.6% Answer Satisfaction, which shows a '
                              'much higher level is achievable. The Others result is a warning sign, but it rests on '
                              'too few responses to act on alone.',
            'recommendation': 'Run **peer-learning sessions** that pair English-queue agents with top Spanish-queue '
                              'agents to share how they explain answers and next steps. Put the **English queue first '
                              'in the weekly QA sample**. For the Others queue, check interpreter and language-line '
                              'handoffs and track the queue over the next campaign before making changes.'},
 'heatmap': {'description': 'A heat map of the % of callers rating each survey question 1–2, by week (Monday start). '
                            'Darker red means more negative ratings. The number of responses per week is shown under '
                            'each week.',
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
                               'not prepared for.'},
 'exceptions': {'description': 'A detailed table with one row per day that had at least 15 responses. It shows that '
                               "day's KPIs and a status flag with the reason: **✖ Critical** (CSAT < 70% or Answer < "
                               '55%), **▲ Warning** (CSAT < 80%, Answer < 60% or Wait OK < 75%) or **✔ OK**. The '
                               "response bar shows each day's volume.",
                'insight': 'Of 15 rated days, **10 are OK, 4 are Warning and 1 is Critical**. The Critical day is '
                           '**Tuesday Nov 18** (CSAT 66.7%, Answer 45.8%, Wait 70.8%, n = 24). The Warning days are '
                           '**Wednesday Nov 5, the campaign launch** (CSAT 77.2%, Answer 58.4%, Wait 70.3%, the lowest '
                           'wait score of any rated day), and **Nov 16, 17 and 19**. The other 29 days had too few '
                           'responses to rate.',
                'interpretation': 'Problems clustered at two moments: **campaign launch** (wait-time pressure) and the '
                                  '**Nov 16–19 run**, when both answer quality and wait time fell. This tells '
                                  "supervisors exactly which dates' schedules and call recordings to pull.",
                'recommendation': 'For every Warning or Critical day, the duty supervisor records a **short cause note '
                                  'within 24 hours** (staffing gap, system issue, unusual call topic). Compare actual '
                                  'staffing around Nov 5 and Nov 16–19 against forecast. Use this report as the '
                                  '**standing agenda for the morning huddle**.'},
 'followup': {'description': 'A transaction-level table of the 15 most recent low-score responses (Overall 1–2 or NPS '
                             '0–6). Each row shows the five ratings (1–2 shaded red, 3 grey), the NPS, the weakest '
                             'service driver and a priority: **High** = Overall 1 or NPS 0–3, **Medium** = all other '
                             'low-score responses.',
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
                                'each scale more clearly) rather than treating them as agent performance issues.'}}

LOWER_SUMMARY = [('CSAT is on target (81.9%) and dissatisfied callers fell by 22, but **Answer Satisfaction slipped to 66.6% (−2.1 '
  'pt)**, the weakest and most negative question (16.8% rated 1–2)',
  'Make Answer Satisfaction a tracked daily KPI with its own target (≥ 70%)',
  'Floor supervisors'),
 ('Callers rate agents highly (90.6% positive) but not the answer; Answer is the lowest rating in **76.8%** of '
  'low-score responses',
  'Weekly QA sample of Answer 1–2 calls; update knowledge-base articles and scripts for recurring topics; coach on '
  'explaining next steps',
  'QA leads'),
 ('The **English queue** (75.5% of volume) is the only queue below target (79.5%) and holds **86%** of dissatisfied '
  'callers; Spanish reaches 90.8%',
  'Peer learning between English and Spanish queue agents; English queue first in the QA sample',
  'Team leads'),
 ('Problems clustered at **launch (Nov 5)** and in a **4-day run below target (Nov 16–19)**, with a Critical day on '
  'Nov 18',
  'Two consecutive reliable days below 80% trigger an escalation; record a cause note within 24 h for each flagged day',
  'Duty supervisor'),
 ('**233 low-score responses** (139 High priority) need follow-up; 50 contradictory responses point to scale confusion',
  'Review High-priority calls within 48 h with root-cause tags; send scale confusion to the survey design team',
  'QA leads')]

MIDDLE = {
    "kpi": {
        "description": "Four KPIs head the page. **Surveys analysed** is the number of survey responses. **CSAT (% favorable)** is the share answering Agree or Strongly Agree to the overall satisfaction question. **Net Promoter Score (NPS)** is the percentage of promoters (9–10) minus the percentage of detractors (0–6) on the 0–10 recommendation question. **% Unfavorable** is the share answering Disagree or Strongly Disagree to overall satisfaction.",
        "insight": "**80.9%** of callers were satisfied, and an NPS of **+53** shows promoters clearly outnumber detractors. Quarterly CSAT has stayed within about 77–84% for five years. The **12.8%** unfavorable rate is steady across campaigns, which points to a recurring issue rather than a one-time problem. Answer satisfaction is the weakest driver at **66.3%** favorable, so better issue resolution offers the biggest gain.",
        "interpretation": "The call center serves most callers well but has stopped improving. Across **28,790** surveys, 80.9% of callers were satisfied and promoters clearly outnumber detractors, so the service is solid and reliable. The remaining 12.8% were unfavorable, and that share has held steady across campaigns and years, so it looks like a recurring problem rather than a passing one. Results are consistent but flat, so the next gains must come from targeted improvement, especially in how well callers' issues are resolved.",
        "recommendation": "Maintain current service levels, set a target (for example, CSAT above 85%), and direct training and process improvements at answer quality and first-call resolution.",
    },
    "trend": {
        "description": "Two line charts share one quarter axis, from 2020Q4 to 2025Q4: CSAT (% favorable) on top and NPS below. Quarters with fewer than 200 responses are hidden. Each chart has its own scale.",
        "insight": "CSAT is flat. It stays within about 77–84% over the five years, with no clear upward or downward trend. The low points are 2021Q3 (76.9%) and 2023Q1 (76.8%), when NPS also fell to about 45. The high points are 2024Q1 (84.4% CSAT) and 2023Q2 (NPS about 62). NPS swings more than CSAT, moving between roughly 45 and 62 and often jumping several points from one quarter to the next. The two lines usually move together: the 2023Q1 dip and the 2023Q2 rebound show up in both.",
        "interpretation": "Service quality has been consistent but has not improved. The 2023Q1 dip and quick recovery look like a short disruption, such as a staffing or process issue, rather than a lasting decline. Quarter-to-quarter NPS moves should be read with caution, since small changes can be random. The recent quarters (2024Q2 to 2025Q4) hold steady at about 80–83% CSAT, so there is no sign of a recent decline.",
        "recommendation": "Investigate 2023Q1: find out what happened (staffing, volume, policy changes) and put safeguards in place so it does not recur. Set a target, for example CSAT above 85%, to move beyond the 77–84% range. Treat CSAT moves of about 4 points or less as normal variation and flag only larger drops. Since overall results are flat, target the weakest driver (answer satisfaction) to lift CSAT.",
    },
    "drivers": {
        "description": "A horizontal bar chart shows the percentage of respondents answering Agree or Strongly Agree on each of the five survey questions, sorted from highest to lowest. The orange bar marks the lowest result, and the dotted line is the average across the five bars.",
        "insight": "Agent Customer Service is the strongest driver at **89.5%** favorable, followed by Agent Job Knowledge (**84.2%**) and Wait Time (**82.5%**), all above the average line, while Overall Satisfaction (**80.9%**) sits near it. Answer Satisfaction is the clear weak spot at **66.3%**, about 15 points below overall satisfaction and 23 points below the best driver.",
        "interpretation": "Callers rate the people and the process well: agents are courteous, knowledgeable and reasonably quick. They are noticeably less happy with the answer or outcome they receive, so the service experience is good but the resolution often falls short. Job Knowledge (r = 0.73) and Answer Satisfaction (r = 0.69) are also the two drivers most strongly correlated with overall satisfaction, so they matter most for the final score.",
        "recommendation": "Make answer quality the top priority, with a target such as raising answer satisfaction from 66% to 75% or higher. Improve first-call resolution through a better knowledge base, clearer scripts and faster escalation for complex cases, and invest in agent job knowledge. Review low-rated calls to learn why answers disappoint (policy limits, wrong information or unmet expectations). Keep current practices for agent service and wait time, since both are working well.",
    },
    "campaigns": {
        "description": "A 100% stacked horizontal bar chart shows how the five overall satisfaction responses split within each survey campaign (Pilot, then Campaigns 1 to 5). Each bar adds up to 100% of that campaign's responses. Colors run from red (Strongly Disagree) through grey (Neutral) to dark blue (Strongly Agree). Labels appear only on segments of 8% or more; hover for the rest.",
        "insight": "The campaigns look almost identical. Strongly Agree is 53–57% of responses in every campaign and Agree 24–28%, so favorable responses land at about 80–82% across the board. Campaign 4 is the highest at about 82%, and Campaign 3 is the lowest at 79.7%. Strongly Disagree holds steady at 8–10%, and Neutral is no more than about 7% in any campaign. The Pilot has the smallest Strongly Agree share (53%) but the largest Agree share (28%), so its favorable rate matches the others.",
        "interpretation": "Satisfaction did not change noticeably from one campaign to the next, so no campaign stands out as clearly better or worse. Callers tend to feel strongly, either very satisfied or very dissatisfied, and few sit in the middle. The unfavorable group (about 13%) has not shrunk since the Pilot, which suggests a lasting issue in service delivery rather than a problem tied to one campaign.",
        "recommendation": "Treat the dissatisfied group as one ongoing problem and analyse it across all campaigns. Start by finding what drives Strongly Disagree responses, especially answer satisfaction and job knowledge ratings, together with call types. Campaign 4 has the highest favorable share and the lowest Strongly Disagree share, so check whether anything in its approach can be repeated. Test any future change against the 80–82% favorable baseline.",
    },
    "languages": {
        "description": "A bubble chart compares language groups with at least 100 responses. The x-axis is % favorable on answer satisfaction and the y-axis is % favorable on overall satisfaction. Bubble size is survey volume, color is the group's NPS (darker = higher), and the dashed line is a trend line fitted through the groups.",
        "insight": "Spanish speakers are the happiest group: about 86% overall, 77% on answer satisfaction and the highest NPS (+74). English speakers are the largest group (23,189 surveys) and the least satisfied overall at about 80%, with answer satisfaction of about 64%. Russian speakers are the clear outlier, with only about 43% favorable on answer satisfaction, even though their overall satisfaction (about 82%) is not low. The two Chinese groups are similar (about 85% overall, 76% answer) but have a low NPS of about 42–48.",
        "interpretation": "Answer and overall satisfaction tend to move together, but not perfectly. The Russian group shows callers can be fairly satisfied overall while unhappy with the answers, which may point to language or interpretation barriers. The Chinese groups show the opposite problem: good satisfaction but low willingness to recommend. English speakers dominate the volume, so they set the overall KPIs. Two cautions: the y-axis is zoomed in, so gaps look larger than they are, and the groups other than English and Spanish have fewer than 500 surveys each. The trend line rests on only five points, so do not read it as a firm relationship.",
        "recommendation": "Review Russian-language service first: interpreter quality, translated scripts and the accuracy of information given. Investigate why the Chinese groups have a low NPS despite good satisfaction, for example through follow-up questions. Study Spanish-language service for practices other groups can use. Improving English-language answer quality would raise overall CSAT the most. Collect more responses from smaller language groups to make future comparisons more reliable.",
    },
}

TOP = {
    "volume": {
        "description": "A month-by-year heat map shows how survey responses were distributed (each cell: count and % of that year), next to a line chart of total responses per year from 2020 to 2025.",
        "insight": "Survey capture grew from **1,004** records in 2020 to a peak of **6,465** in 2024 (6,025 in 2025). After irregular scheduling in 2020 and 2021, collection settled by 2023 into five concentrated anchor months: January, May, July, September and November. Peak months hold about 1,000–1,200 responses, while off-months drop to near zero.",
        "interpretation": "The uneven monthly pattern is not a data gap but a deliberate design. NYC Local Law 26 of 2021 requires NYC311 to run at least five customer-satisfaction survey campaigns a year. Invitations go out in bursts during launch months, with small spillover into the following month.",
        "recommendation": "Because the data are five concentrated snapshots a year rather than a continuous sample, executives should compare performance campaign over campaign (for example, the May cohort against the July cohort) rather than month over month, since off-months lack enough volume to be meaningful.",
    },
    "tree": {
        "description": "A feature-importance bar chart sits beside a three-level decision tree that classifies callers into NPS groups (Detractor 0–6, Passive 7–8, Promoter 9–10) from their five ratings and the survey turnaround time. Each tree node shows its split, its share of callers and its NPS mix.",
        "insight": "Overall Satisfaction carries **87.7%** of the model's importance, followed distantly by Answer Satisfaction at **10.0%** and Agent Customer Service at 2.3%. Turnaround, Wait Time and Job Knowledge carry essentially **0%**. The tree shows a hard threshold: when both Overall and Answer Satisfaction are 3 or lower (≤ 3.5), a segment of **16.6%** of callers lands in the Detractor zone.",
        "interpretation": "Top-level NPS is gated by getting a satisfactory answer. Backend timing, such as how long the survey took to complete, has virtually no influence on whether a caller recommends 311.",
        "recommendation": "Do not prioritise strategic investment in shorter backend turnaround, since it does not move NPS. Set service standards so callers do not leave an interaction with Answer Satisfaction below 4.",
    },
    "apriori": {
        "description": "An executive summary built with target-oriented association rule mining (Apriori, minimum support 5%, minimum confidence 30%). It maps combinations of caller ratings to the NPS segment they predict, shown as Reliability (confidence), Customer Share (support) and Impact (lift: how many times more likely than average).",
        "insight": "A perfect 5/5 across all five questions predicts a Promoter with **97.6%** reliability and covers **28.9%** of callers. At the other end, Answer Satisfaction of 1/5 is the most severe pain point: it predicts a Detractor with **66.4%** reliability, **4.04×** more likely than average.",
        "interpretation": "Answer quality anchors customer sentiment. Even when agents are polite and waits are short, an unsatisfactory answer will very likely turn the caller into a Detractor. Passives are a conversion opportunity: they often rate overall satisfaction 4/5 but are held back by average job knowledge or wait time.",
        "recommendation": "Shift strategic budget from general customer-service etiquette training to first-contact resolution and technical job-knowledge programs. Set a top-level KPI to eliminate 1/5 Answer Satisfaction interactions.",
    },
}
