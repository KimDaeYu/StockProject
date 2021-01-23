from slacker import Slacker
token = 'xoxb-1643665366434-1628895511927-500UBA6wPmzmClzmUb5wrddS'
slack = Slacker(token)
#slack.chat.post_message('#stock-talk', 'message', as_user=True)
slack.chat.post_message('#stock-talk', 'Hello fellow slackers!')
#response = slack.users.list()
#print(response)

attachments_dict = dict()
attachments_dict['pretext'] = "attachments 블록 전에 나타나는 text"
attachments_dict['title'] = "다른 텍스트 보다 크고 볼드되어서 보이는 title"
attachments_dict['title_link'] = "https://corikachu.github.io"
attachments_dict['fallback'] = "클라이언트에서 노티피케이션에 보이는 텍스트 입니다. attachment 블록에는 나타나지 않습니다"
attachments_dict['text'] = "본문 텍스트! 5줄이 넘어가면 *show more*로 보이게 됩니다."
attachments_dict['mrkdwn_in'] = ["text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.
attachments = [attachments_dict]

slack.chat.post_message(channel="#stock-talk", text=None, attachments=attachments, as_user=True)