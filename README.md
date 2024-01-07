### Sentiment analysis for U.S. interconnection queues

#### Background

The volume of capacity in Independent System Operator/Regional Transmission Organization interconnection queues across the U.S. is at an all-time high, with approximately 947 GW from solar projects and approximately 300 GW from wind projects [(Lawrence Berkley National Lab)](https://emp.lbl.gov/news/grid-connection-requests-grow-40-2022-clean).

However, as projects progress through queues sequentially, if a project further along in a queue withdraws, this may adversely affect later projects. For example, later projects might rely on a previous project to shoulder expensive infrastructure upgrade costs that make these later projects financially feasible. Thus, if a previous project withdraws, later projects might have to withdraw as well, creating a ripple effect. This uncertainty leads developers to apply to different queues simultaneously and only develop whichever project might be most profitable.

Therefore, if developers had greater insight into the probability of successful development of other projects, they might be less likely to flood the queue with place-holding projects, committing more decisively to fewer projects. This would reduce queue volumes and simplify queue study processes for ISO/RTOs. 

A growing body of academic research studies community opposition to renewable energy projects, and the role this opposition plays in development success or failure.
[Stokes et al. (2023)](https://www.pnas.org/doi/10.1073/pnas.2302313120) find that opposition is present in 17% of their sample of wind energy projects in the United States, and 18% in Canada, between 2000 and 2016. They find population ethnicity, population wealth, and project size to be determining factors. Larger projects are more likely to be opposed, and in the United States, opposition is more likely in areas with a higher proportion of White people, and a lower proportion of Hispanic people; in Canada, the same pattern holds for wealthier communities.
[Bessette and Mills (2021)](https://www.sciencedirect.com/science/article/abs/pii/S2214629620304485) use a wind contention survey of 46 energy professionals to assess 69 US wind farms and find characteristics that may predispose communities to oppose wind farms. They find a greater proportion of production-oriented farming and fewer natural amenities in a community are associated with reduced wind farm opposition. They also find communities with a greater percentage of residents that voted Republican in the 2016 Presidential election demonstrate less opposition. 
[Susskind et al. (2022)](https://www.sciencedirect.com/science/article/pii/S0301421522001471) study 53 wind, solar, and geothermal energy projects that were delayed or blocked between 2008 and 2021, identifying seven sources of opposition: 1. Concerns over possible environmental impacts, including impacts on  wildlife; 2. Challenges to project financing and revenue generation; 3. Public perceptions of unfair participation processes or inadequate inclusion in light of regulatory requirements; 4. Failure to respect Tribal rights, including the right to consultation; 5. Health and safety concerns; 6. Intergovernmental disputes; 7. Potential impacts on land and property value.

There is no consensus on which characteristics may be predictive of community opposition. However, other researchers suggest social media plays an important role. [Fergen et al. (2021)](https://www.sciencedirect.com/science/article/abs/pii/S2214629621003170) suggest social media plays a role in reinforcing negative sentiment, while [Winter et al. (2022)](https://www.nature.com/articles/s41560-022-01164-w) found, "moderate-to-large relationships between various indices of conspiracy beliefs and wind farm opposition".

In this project, I set out to confirm variables predictive of renewable energy development opposition suggested in the literature, while exploring new data (such as the spread of misinformation through community Facebook pages) that might lead to increased opposition. As an early iteration, I focus on wind projects. My objective is to build a model that outputs opposition risk for new projects in U.S. interconnection queues. 

#### Code

- coordinate_locator.py: Finds coordinates for towns in the interconnection queue, used for the front end map 
- corr_amenity_queues.py: Takes processed in-service and withdrawn wind projects and calls models from models.py
- data_merger.py: Merges and formats project data with other data of interest
- geojson_creator.py: Creates geojson file for Mapbox using towns in the interconnection queue
- geojson_publisher.py: Uploads a geojson file to Mapbox via APIs
- helpers.py: Helper functions (mainly for .csv operations)
- models.py: Contains model training and testing data
- model_helpers.py: Contains helper functions for models.py
- natural_amenity_parser.py: Parses and preprocesses natural amenity data
- queue_parser.py: Parses and preprocesses offline interconnection queues, creating CSVs of active, in-service, and withdrawn projects with cleaned county names and project type indicators
- bryce_parser.py: Parses offline list of opposed projects from [Robert Bryce](https://robertbryce.com/renewable-rejection-database/)
- state_names.py: Contains dictionaries of state names for data cleaning
