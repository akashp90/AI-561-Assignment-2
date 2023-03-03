-- video_created_at_week_wise
SELECT c.id as upper_channel_id FROM channels c
WHERE 5 = (SELECT count(week_no) FROM 
(
	SELECT WEEK(created_at) AS week_no, channel_id, count(*) as v_count FROM videos 
	WHERE created_at
	BETWEEN DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y-%m-01 00:00:00')
	AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59')
	AND channel_id = c.id
	GROUP BY 1,2
)AS counted);