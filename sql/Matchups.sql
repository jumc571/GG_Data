SELECT 
	opp_char as Character
	, round(SUM(cast(wins as float))/SUM(wins + losses) * 100, 2) as [Win %]
	, SUM(cast(SUBSTRING(opp_rating, 1, 4) as int)) / count(1) as [Avg Rating]
	, SUM(wins + losses) as Volume
  FROM [GG].[dbo].[Games]
  Group By opp_char