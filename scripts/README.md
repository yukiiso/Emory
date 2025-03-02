プロジェクトのセットアップや管理を簡単にするためのスクリプトを置く場所

[Localhost Flask API Health Check](http://localhost:5001/api/health)

[Localhost Frontend Sign Up](http://localhost:3000/sign-up)

[Localhost Frontend Talk](http://localhost:3000/talk)

[Localhost Frontend Search](http://localhost:3000/search)

[Ngrok Flask Health Check](https://defe-142-231-179-140.ngrok-free.app/health)

[EC2 Flask](http://15.223.119.153:5001/api/db/sql/User)

[EC2 Frontend](http://15.223.119.153:3000/talk)

[EC2 Secure Flask](https://15.223.119.153/api/db/sql/User)

[EC2 Secure Frontend](https://15.223.119.153/talk)


AWS Transcribe and Comprehend Demo: 
```
curl -X POST http://localhost:5001/api/transcribe/start_transcription \
     -H "Content-Type: application/json" \
     -d '{"s3_uri": "s3://emory-app-bucket/video.mp4", "output_bucket": "emory-app-bucket"}'
```

ChatGPT: 
```
curl -X POST http://localhost:5001/api/chatgpt/summary \
     -H "Content-Type: application/json" \
     -d '{
           "text": "During our last session, the client expressed a deep sense of frustration regarding their work-life balance. They mentioned that despite trying to manage their time effectively, they often feel overwhelmed by the constant demands from their job and the pressure to meet deadlines. This has been affecting their ability to enjoy personal time, and they fear it is starting to impact their overall well-being, both physically and emotionally. The client also shared that they are seeking strategies to better manage stress and improve their productivity without sacrificing their mental health."
         }'
```