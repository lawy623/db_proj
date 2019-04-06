1. Account Use: yl4003.

2. URL: http://34.73.134.125:8111/

3. As stated in our proposal, we implement the visualization of our football database. That it shows
 all the information in the database, and it allows the kinds of redirection by hyperlink, which explore 
 the relationship between tables. We also  provide a simple way of adding data to the database, such as 
 adding new players and add new match records. 
 In conclusion, we implement all the things we mentioned in our proposal.

4.
(a) The page of add_record:
This page will get the information about this match, and it will fetch all the existing players of both team.
Then user can add the score record for those players. Those records will be insert to the database
(to score table), and many pages will be affected by the update of this match record(e.g. Player's info page,
league score leading board, etc.) which is quite interesting.

(b) The page of score leading board:
In this page, we get the leading board for each league. It will sum up the goals that a specific person scores,
and order them by the number. Also it will relate the player to the team it belongs to. This involves operations
inclding Group By, Order By, Join, Aggregation, etc.
 