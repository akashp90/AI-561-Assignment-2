SELECT mv.video_id_1, uvv.video_id FROM marvel_videos mv 
LEFT JOIN user_video_views uvv ON mv.video_id_1 = uvv.video_id