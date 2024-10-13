import json
import logging
import pathlib
import os
import concurrent.futures
import toml
import anthropic
import tqdm
from patcher.translator import Claude3Api

dialogue_keys = ['SDM_1104904126#0',
 'SDM_2104023601#0',
 'TNPC_70002451#29',
 'SDM_2101057301#0',
 'TNPC_70001001#7',
 'SDM_1101761201#0',
 'TNPC_08002151#0',
 'TNPC_60075540#0',
 'SDM_2102037401#0',
 'TNPC_31038201#0',
 'SDM_2102042901#0',
 'SDM_1101626506#0',
 'SDM_1101732207#0',
 'TNPC_10003741#0',
 'SDM_1101042201#0',
 'TNPC_20056001#0',
 'TNPC_20057001#0',
 'TNPC_60080550#0',
 'TNPC_31037001#0',
 'TNPC_20079001#1',
 'TNPC_60074300#1',
 'TNPC_70008521#9',
 'SDM_1101042316#0',
 'SDM_2101061501#0',
 'TNPC_30070051#0',
 'TNPC_60076640#0',
 'SDM_2101000101#1',
 'SDM_310415027#0',
 'TNPC_31087401#0',
 'SDM_1104706521#0',
 'TNPC_20109028#0',
 'SDM_2102030301#0',
 'TNPC_31030301#0',
 'SDM_2104005701#0',
 'SDM_2104017501#0',
 'TNPC_10003721#0',
 'SDM_2103024701#0',
 'TNPC_70001001#13',
 'TNPC_70002451#98',
 'TNPC_70002451#1',
 'TNPC_70002451#3',
 'SDM_3101501110#0',
 'SDM_2101061101#0',
 'SDM_2102043101#0',
 'SDM_2104023801#0',
 'TNPC_31080401#0',
 'TNPC_20101001#0',
 'SDM_2102024401#0',
 'SDM_2102004401#0',
 'SDM_2101059001#0',
 'TNPC_20062001#0',
 'TNPC_60074975#0',
 'TNPC_20034001#0',
 'TNPC_60077310#0',
 'TNPC_10003714#0',
 'TNPC_31077201#0',
 'SDM_3101802301#0',
 'SDM_2102046301#1',
 'TNPC_16001241#0',
 'SDM_1101761216#0',
 'SDM_2101060901#0',
 'TNPC_31034401#0',
 'TNPC_31081201#0',
 'TNPC_50005751#0',
 'TNPC_60080650#0',
 'TNPC_10003711#0',
 'TNPC_60080570#0',
 'TNPC_31094001#0',
 'SDM_2102023201#0',
 'SDM_2102042401#0',
 'TNPC_10003793#0',
 'SDM_3101803001#0',
 'SDM_2102043601#0',
 'TNPC_70008521#12',
 'SDM_3104150301#0',
 'TNPC_60075320#0',
 'TNPC_70002451#2',
 'TNPC_10003761#0',
 'SDM_1101752111#0',
 'fix_2104014401#0',
 'SDM_2102030101#0',
 'TNPC_31037101#0',
 'SDM_1101042417#0',
 'SDM_1101918801#0',
 'TNPC_60076515#0',
 'TNPC_70002451#4',
 'SDM_3101501301#0',
 'TNPC_60074300#0',
 'TNPC_60075350#0',
 'SDM_3101804532#0',
 'SDM_2102043801#0',
 'TNPC_70008521#1',
 'TNPC_31035011#0',
 'SDM_2103024801#0',
 'SDM_1104707601#0',
 'TNPC_20051001#0',
 'TNPC_60076575#0',
 'TNPC_70001001#11',
 'SDM_1101042222#0',
 'SDM_2101058901#0',
 'TNPC_20059001#0',
 'TNPC_70001001#14',
 'TNPC_30070041#0',
 'TNPC_70002451#9',
 'SDM_1101780376#0',
 'TNPC_31050301#0',
 'SDM_2102033801#0',
 'SDM_1104008401#0',
 'SDM_2101059201#0',
 'SDM_1104007941#0',
 'SDM_2102016101#0',
 'TNPC_30070011#0',
 'SDM_3101820001#0',
 'TNPC_31010051#0',
 'TNPC_70008521#3',
 'SDM_1104101716#0',
 'SDM_2102042501#0',
 'TNPC_20055001#0',
 'SDM_2102046301#0',
 'SDM_1101042526#0',
 'TNPC_31032101#0',
 'SDM_2102043001#0',
 'TNPC_31081101#0',
 'SDM_1104009106#0',
 'SDM_1104720241#0',
 'SDM_2102015301#0',
 'TNPC_30047000#0',
 'SDM_1101761321#0',
 'TNPC_20076001#0',
 'SDM_1101034301#0',
 'SDM_2102035501#0',
 'TNPC_20075001#0',
 'SDM_2102008201#0',
 'SDM_1101042301#0',
 'SDM_3101819701#0',
 'SDM_1101042421#0',
 'SDM_2102042701#0',
 'TNPC_08002350#0',
 'TNPC_31054001#0',
 'TNPC_31067301#0',
 'SDM_2102030101#1',
 'TNPC_70002451#11',
 'TNPC_70002000#7',
 'SDM_3101809701#0',
 'TNPC_31032401#0',
 'TNPC_70002451#99',
 'SDM_1101761241#0',
 'TNPC_70008521#7',
 'TNPC_20079001#0',
 'SDM_2102043901#0',
 'TNPC_70002451#22',
 'SDM_2102029701#0',
 'TNPC_70002451#50',
 'TNPC_10003781#0',
 'TNPC_70002000#6',
 'SDM_1101042101#0',
 'SDM_2101055301#0',
 'SDM_1101733011#0',
 'SDM_2101059101#0',
 'SDM_2102002701#0',
 'TNPC_31035301#0',
 'TNPC_10003701#0',
 'TNPC_60074200#0',
 'TNPC_70002451#0',
 'SDM_2102029901#0',
 'TNPC_20074001#0',
 'SDM_2104021401#0',
 'TNPC_31077001#0',
 'SDM_1104707701#0',
 'TNPC_70002451#13',
 'TNPC_70002451#87',
 'TNPC_31080701#0',
 'SDM_1101732001#0',
 'SDM_2101057601#0',
 'TNPC_70002451#48',
 'SDM_1101791411#0',
 'SDM_2102004301#0',
 'TNPC_20052001#0',
 'SDM_2104013801#0',
 'SDM_3104151301#0',
 'TNPC_70002451#96',
 'TNPC_17025977#0',
 'SDM_2104018101#1',
 'SDM_1101603901#0',
 'TNPC_70002451#51',
 'SDM_2102004901#0',
 'TNPC_08002421#0',
 'SDM_2104023801#1',
 'fix_2104013801#0',
 'SDM_2102011001#0',
 'TNPC_60074975#1',
 'SDM_2102034401#0',
 'SDM_2104013501#0',
 'TNPC_60080560#0',
 'SDM_1101042401#0',
 'fix_90001001#0',
 'TNPC_31081501#0',
 'TNPC_60074840#0',
 'SDM_1101791436#0',
 'SDM_2102004701#0',
 'TNPC_20061001#0',
 'SDM_2102022701#1',
 'SDM_1101042312#0',
 'SDM_2102010101#0',
 'SDM_3101817701#0',
 'TNPC_20060001#0',
 'TNPC_60072249#0',
 'SDM_310415061#0',
 'TNPC_60078300#0',
 'TNPC_70002451#17',
 'SDM_3104150601#0',
 'SDM_2101061601#0',
 'TNPC_31033001#0',
 'TNPC_70002451#97',
 'TNPC_70008521#24',
 'SDM_2102009901#0',
 'TNPC_20078001#0',
 'SDM_2102042601#0',
 'SDM_2101063201#0',
 'SDM_1101623233#0',
 'SDM_3101047033#0',
 'TNPC_20048001#0',
 'TNPC_17025954#0',
 'SDM_2102024701#0',
 'TNPC_20053001#0',
 'TNPC_60078540#0',
 'TNPC_31040301#0',
 'SDRAMA_3101045901#0',
 'SDM_3104004001#0',
 'SDM_1104007916#0',
 'TNPC_70002451#49',
 'TNPC_70001001#8',
 'SDM_1101042501#0',
 'SDM_2102046001#0',
 'SDM_1101733001#0',
 'SDM_2103013001#0',
 'SDM_1104007701#0',
 'SDM_3104150310#0',
 'SDM_2102009601#0',
 'TNPC_30084001#0',
 'SDM_1101042211#0',
 'SDM_2102002201#0',
 'SDM_2101000101#0',
 'TNPC_31035201#0',
 'TNPC_70001001#9',
 'TNPC_31052101#0',
 'SDM_1101042226#0',
 'TNPC_70001001#10',
 'TNPC_70008521#10',
 'SDM_3103009601#0',
 'TNPC_31037201#0',
 'SDM_1101761301#0',
 'TNPC_30042001#0',
 'SDM_1101761231#0',
 'TNPC_08002251#0',
 'SDM_2101064301#0',
 'TNPC_31037301#0',
 'HEAR_20173001#0',
 'SDM_1101042111#0',
 'SDM_2101064601#0',
 'SDM_2102028501#1',
 'TNPC_60078430#0',
 'TNPC_70002451#10',
 'SDM_2103019501#0',
 'SDM_1104904601#0',
 'SDM_1101042411#0',
 'SDM_2104019201#0',
 'SDM_3104150701#0',
 'SDM_2102043201#0',
 'TNPC_31030201#0',
 'SDM_2104013901#0',
 'SDM_2102024601#0',
 'SDM_2102043701#0',
 'SDM_1101042116#0',
 'SDM_1104008656#0',
 'TNPC_10003126#0',
 'TNPC_31020001#0',
 'TNPC_31043201#0',
 'SDM_2104011601#0',
 'SDM_1101042517#0',
 'SDM_1101032431#0',
 'SDM_1101042511#0',
 'SDM_31018172101#0',
 'TNPC_31018001#0',
 'TNPC_31050001#0',
 'TNPC_60079050#0',
 'TNPC_20077001#0',
 'TNPC_60075500#0',
 'TNPC_70008521#4',
 'SDM_2102016901#0',
 'TNPC_31080901#0',
 'SDM_2102024501#0',
 'TNPC_70001001#6',
 'SDM_2101063301#0',
 'SDM_2104020801#0',
 'TNPC_20109028#1']

dialogue_keys = ['untranslated_0',
 'untranslated_1',
 'untranslated_2',
 'untranslated_3',
 'untranslated_4',
 'untranslated_5',
 'untranslated_6',
 'untranslated_7',
 'untranslated_8',
 'untranslated_9',
 'untranslated_10',
 'untranslated_11',
 'untranslated_12',
 'untranslated_13',
 'untranslated_14',
 'untranslated_15',
 'untranslated_16',
 'untranslated_17',
 'untranslated_18',
 'untranslated_19',
 'untranslated_20',
 'untranslated_21',
 'untranslated_22',
 'untranslated_23',
 'untranslated_24',
 'untranslated_24',
 'untranslated_25',
 'untranslated_26',
 'untranslated_27',
 'untranslated_28',
 'untranslated_29',
 'untranslated_30']


def test_function():
    test_prompt = (
        "이것은 테스트 프롬프트입니다. 제가 hello라고 하면 world라고 응답해주세요."
    )
    test_first_return = "네, 이것은 테스트 프롬프트에 대한 첫 번째 응답입니다."
    test_text = "hello"
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)
    claude_response = claude.translate(test_prompt, test_first_return, test_text)
    assert claude_response.content[0].text == "world"
    print(claude_response.content[0].text)


def test_function2(api_key):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=api_key,
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1001,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '당신은 중국어 무협 텍스트를 한국어로 번역하는 전문가입니다. 중국에서 제작된 무협 게임의 스크립트들을 한국어로 번역할 것입니다.\n제공될 텍스트는 고룡(古龍)작가의 무협 세계관을 기반으로 한 게임 고룡풍운록(古龍風雲錄)의 스크립트들입니다. 그의 특징적인 문체를 살리세요.\n게임 플롯 : 진우(辰雨)는 구주왕심천군(九州王沈天君)이 인의장(仁義莊)에 데려온 출신을 알 수 없는 서동(書童)이었습니다.\n전 장주였던 심천군은 형산(衡山) 회안봉(回雁峰)에 무적검전(無敵劍典)이 있다는 소문으로 벌어진 음모에 휘말려 죽었고 이후 십년이 지났습니다.\n최근 연남천(燕南天)의 장보도가 있다는 소문이 돌자 음모의 연관성을 의심한 냉이(冷二)가 그를 강호로 보내 사건을 조사하며 음모를 밝히는 내용의 RPG입니다.\n주인공 설정 : 진우(辰雨)는 한때 인의장의 그림자 같은 인물로, 감정이 메마르고 말이 적으며, 출신내력이 불명하다. 옛 장주의 유언에 따라 직무를 맡거나 장을 나가는 것, 손을 쓰면 안 된다는 규칙을 지켜왔다. 회안봉 사건 십년이 지나서야 강호에 발을 들였다.\n\n주요 등장인물 설정:\n심랑 : 심천군의 아들로 명가자제다운 품격과 소탈함이 있다. 예의가 바르고 남을 안심시킨다.\n\n주칠칠 : 주가 활재신의 영애로 아름답고 정의감이 뛰어난 당찬 여성이다.\n\n강소어 : 악인곡에서 십대악인에게 길러진 소년으로 장난이 심하고 자신감이 넘친다.\n\n초류향 : 답월류향의 경공으로 유명한 우아한 군자, 도적으로 알려져 있지만 정의롭고 사람을 해치지 않는다.\n\n이심환 : 소이비도로 유명하며 진사와 탐화를 여러번 배출한 유명한 가문의 후손이지만 십년전 명예를 버리고 은둔한 남자다. 현재 건강도 좋지 않아 기침을 많이 하지만 여전히 눈빛은 살아있는 대협이다.\n\n백비비 : 쾌활왕 시옥관에게 복수하고 싶어하는 아름다운 여성으로 사실 유령궁주의 신분을 숨기고 있다.\n\n금무망 : 금가의 장남으로 스스로 얼굴을 망가뜨리고 기관비술에 전념했다. 한 때 쾌활왕 측근 재사로 있었다.\n\n손소홍 : 손백발 노인의 손녀로 땋은 머리를 한 귀여운 소녀, 노래 대신 이야기를 하며 재주를 판다. 자신만의 이야기를 만들고 싶어한다.\n\n임선아 : 천하제일미녀\n\n왕련화 : 낙양의 지하성주이자 뛰어난 재능을 가진 남자로 배운 것이 많아 천면공자라고도 불린다. 선악을 알기 어려운 인물로 변장술에 능하다.\n\n육소봉 : 수염이 마치 눈썹같아 사조미모라 불리며 붉은 장포를 걸친 남자다. 지략이 뛰어나지만 말투가 신랄하고 무례하다. 하지만 천하에 친구가 많고 의리를 중시하는 쾌남이다.\n\n공손란 : 여성을 위한 여성만의 비밀조직 홍혜자의 수장으로 손속이 잔인하여 사람들이 두려워한다. 하지만 선녀처 아름다운 누님이다.\n\n소앵 : 차가워보이지만 총명하고 말을 잘하는 소녀다. 무공은 못하지만 지략이 뛰어나고 악인곡의 소마성 강소어의 천적이다.\n\n번역지침\n1. 높임말과 반말, 평서체를 구분해서 사용.\n- 존댓말: 부탁이나 공경의 표현에 사용. 예: "謹聽莊主之命！" → "장주님의 명에 따르겠습니다."\n- 반말: 도발적, 협박적, 고압적인 말투에 사용. 예: "軟柿子，受死吧！" → "나약한 놈, 죽어라!"\n- 평서체: 불확실한 상황이나 상황 설명에 사용. 예: "夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。" → "사이에 끼워진 종이에는, \'양란소진괴랑중(揚瀾小鎮怪郎中)\'이 적혀있다."\n- 위 지침에 어긋나더라도, 맥락을 고려했을 때 더 적합한 표현이 있다면 그것을 사용하세요.\n2. 태그와 플레이스홀더 유지.\n- "{}"안에 있는 내용은 그대로 두세요. 예: "這是{it2000_03}。" → "이것은 {it2000_03}이다."\n- "<>"안에 있는 내용도 번역하지 마세요. 예: "這<color=#FF0000>茶葉</color>你就拿去吧！" → "이 <color=#FF0000>찻잎</color>을 가져가!", "保護<b>{playerName}</b>!" → "<b>{playerName}</b>을/를 보호해!"\n- 태그와 플레이스 홀더는 게임엔진에서 출력될 때 변경되므로 오타나 변경이 있을 경우 게임이 멈출 수도 있습니다. 주의하세요!\n3. 무협세계관 유지.\n- 한글/한자어 사용: 영어에서 유래한 외래어 대신 한글/한자어 사용. 예: "桌子" → "탁자","藏寶圖" → "장보도", "公子" → "공자"\n- 무협지식 호칭에 주의. 예: "大俠" → "대협", "師兄" → "사형", "師姐" → "사저", "俠客" → "협객", "莊客" → "장객", "莊主" → "장주", "兄弟" → "형제", "大哥" → "대가", "哥哥" → "가가" ,"小弟" → "소제", "大爺" → "대야", "小爺" → "소야" 등\n4. 원문 표기.\n- 이름, 지명, 무공, 물건, 별명 등은 음차하고 원문을 병기하여 사용. 예: "辰雨" → "진우(辰雨)", "柴玉關" → "시옥관(柴玉關)", "我在地靈莊。" → "나는 지령장(地靈莊)에 있다.", "秘笈，正陽佛手。" → "비급, 정양불수(正陽佛手)", "這是……嵩陽鐵劍？" → "이건...숭양철검(嵩陽鐵劍)?"\n- 고사성어에서 유래된 표현 등은 뜻을 번역하고 원문을 병기하세요. 예: "漏了<color=#FF0000>果老騎驢</color>四個字。" → "<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노인)</color> 네 글자를 빠뜨렸다."\n- **최종적으로 번역된 결과물에서 병기된 원문은 검수자가 일괄 처리 할 수 있으므로 한자 병기 지침을 항상 준수**.\n5. 문법 및 표현의 자연스러움 재확인.\n잘 지켜진 예: "九年前……你──！你可是朱家的千金？" → "구년 전... 너는──! 혹시 주가의 천금(千金)인가?"\n잘못된 예(문법적으로 어색함):"九年前……你──！你可是朱家的千金？" → "아홉 해 전…… 너는──! 너 혹시 주가(朱家)의 따님인가?"\n6. 번역 중 의미가 모호한 경우 원문의 의도를 가장 잘 전달할 수 있는 표현 선택.\n7. 입력 json 데이터의 포맷 설명.\n- context: 스크립트 속 인물의 정보와 특정 텍스트를 번역하는 방법에 대한 정보 제공.\n예 : 천왕채무리의 정보: 성별은 Male이다.,"天王寨" → "천왕채"\n- talks: 연속된 대화내용이 각 대화의 id를 키값으로 하여 제공됨\n- talker: 발화자의 id, 필요한 경우 context를 통해 id가 누구인지 명시함\n- type: 대화의 종류. Narrator(내레이터), Dialogue(대화), Option(플레이어의 선택지) 등이 있음\n- content : 번역할 텍스트\n- next_talks: 다음 대화의 id 나열. Optional Field\n7. 출력 json 데이터의 포맷설명\n- summarize: 번역된 대화문의 짧은 요약.\n- notify_id: 번역 과정 중 발견된 문제가 있는 텍스트의 ID 나열.\n- content의 번역된 결과를 원본 id를 키로 하여 명시\n입력예 :\n{\n  "context": "벽화가 있는 동굴에 대한 이야기",\n  "talks": {\n   "0001": {\n    "talker": "Narrator",\n    "content": "幽山深谷靜<br>壁畫驚成謎。",\n    "type": "Narrator"\n   },\n   "0002": {\n    "talker": "Player",\n    "content": "此洞江湖人士眾多……",\n    "type": "Dialogue",\n    "next_talks": "0003,0004"\n   },\n   "0003": {\n    "talker": "Option",\n    "content": "進入參悟",\n    "type": "Option"\n   },\n   "0004": {\n    "talker": "Option",\n    "content": "暫且不入",\n    "type": "Option"\n   },\n   "0005": {\n    "conten": "#N/A"\n   },\n   "0006": {\n    "talker": "Narrator",\n    "content": "竟已領悟了壁畫上的{0}武功",\n    "type": "Narrator"\n   }\n  }\n}\n출력예 :\n{\n  "summarize": "벽화가 있는 동굴에서 무공을 얻음, id 5번 데이터 이상",\n  "notifyId": ["0005"],\n  "0001": "고요한 유산심곡(幽山深谷)에<br>수수께끼의 벽화가 남아있다.",\n  "0002": "이 동굴에는 강호인사(江湖人士)가 많다...",\n  "0003": "진입하여 깨달음을 얻는다.",\n  "0004": "일단 들어가지 않는다.",\n  "0006": "자신도 모르게 벽화에 그려진 {0}무공을 깨달았다."\n}\n위의 지침을 바탕으로 번역을 진행해주시기 바랍니다.',
                    }
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "네, 게임의 설정과 각 지침을 숙지했습니다. 데이터를 입력해주세요.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": '{\n  "context": "금전방고수의 성별: Male,금전방무리의 성별: Male,이심환의 성별: Male",\n  "talks": {\n    "0": {\n      "talker": "금전방고수(金錢幫高手)",\n      "content": "小的們，給我上！",\n      "type": "Dialog"\n    },\n    "1": {\n      "talker": "금전방무리(金錢幫幫眾)",\n      "content": "是！",\n      "type": "Dialog"\n    },\n    "2": {\n      "talker": "이심환(李尋歡)",\n      "content": "你們飛少爺人在何處？",\n      "type": "Dialog",\n      "next_talks": "3"\n    },\n    "3": {\n      "talker": "금전방고수(金錢幫高手)",\n      "content": "咳……少爺往……東邊的野林深處……去了。",\n      "type": "Dialog"\n    }\n  }\n}',
                    }
                ],
            },
        ],
    )

    print(message.content)


def batch_process(start_index: int = 0, end_index: int = 1):

    prompt = "당신의 임무는 중국에서 제작된 무협 RPG 게임 \"천명기어\"를 무협 세계관을 유지하면서 한국어로 번역하는 것입니다.\n번역 지침:\n\n말투 구분\n\n존댓말: 부탁이나 공경의 표현에 사용. 예: \"謹聽莊主之命！\" → \"장주님의 명에 따르겠습니다.\"\n반말: 도발적, 협박적, 고압적인 말투에 사용. 예: \"軟柿子，受死吧！\" → \"나약한 놈, 죽어라!\"\n평서체: 불확실한 상황이나 상황 설명에 사용. 예: \"夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。\" → \"사이에 끼워진 종이에는, '양란소진괴랑중(揚瀾小鎮怪郎中)'이 적혀있다.\"\n\n\n태그와 플레이스홀더 유지\n\n\"{}\"안의 내용 유지. 예: \"這是{it2000_03}。\" → \"이것은 {it2000_03}이다.\"\n\"<>\"안의 내용 유지. 예: \"這<color=#FF0000>茶葉</color>你就拿去吧！\" → \"이 <color=#FF0000>찻잎</color>을 가져가!\"\n\n\n무협 세계관 유지\n\n영어에서 유래한 외래어 대신 한글/한자어 사용. 예: \"一掌\" → \"일장\", \"桌子\" → \"탁자\"\n무협식 호칭 주의. 예: \"大俠\" → \"대협\", \"師兄\" → \"사형\", \"師姐\" → \"사저\"\n\n\n한자 병기\n\n이름, 지명, 무공, 물건, 별명에 적용. 예: \"柴玉關\" → \"시옥관(柴玉關)\"\n고사성어는 뜻도 병기. 예: \"<color=#FF0000>果老騎驢</color>\" → \"<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노f인)</color>\"\n\n\n애칭 표현 주의\n\n\"小\"글자로 시작하는 이름은 애칭으로 처리. 예: \"小玥\" → \"소월\", \"小梅\" → \"소매\"\n\"小子\"는 상황에 따라 \"꼬맹이\" 또는 \"애송이\" 등으로 번역\n\n\n메타데이터 활용\n\n제공된 메타데이터의 용어를 우선적으로 사용하여 일관성 있는 번역 유지\n\n\n\n입력 데이터 형식:\n<input>\n{\n\"need_translate\": {\n\"1104904601\": \"중국어 텍스트\",\n\"1104904602\": \"중국어 텍스트\",\n\"1104904603\": \"중국어 텍스트\"\n},\n\"meta_data\": {\n\"용어1\": \"번역1\",\n\"용어2\": \"번역2\"\n}\n}\n</input>\n응답은 다음 <result> 태그 내에 json 형식으로 제공하세요:\n<result>\n{\n\"1104904601\": \"번역 결과\",\n\"1104904602\": \"번역 결과\",\n\"1104904603\": \"번역 결과\"\n}\n</result>"
    first_answer = "네, 이해했습니다. 중국어 무협 RPG 게임 \"천명기어\"의 텍스트를 한국어로 번역하되, 무협 세계관을 유지하고 자연스러운 한국어로 옮기겠습니다. 특수 태그와 알파벳, 숫자는 그대로 유지하고, 대화 상황에 맞는 말투를 사용하며 현대적 용어는 피하겠습니다. 제공된 meta_data가 있다면 참고하여 번역하겠습니다. 번역 결과는 요청하신 JSON 형식으로 제공하겠습니다. 중국어 텍스트를 입력해 주시면 번역을 시작하겠습니다."
    
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)
    for key in tqdm.tqdm(dialogue_keys[start_index:end_index]):
        if os.path.exists(f"./works/{key}.txt"):
            logging.info(f"{key} already exists")
            continue
        logging.info(f"Processing {key}")
        logging.info(json.dumps(dialogues[key], ensure_ascii=False))
        data = claude.translate(
            prompt,
            first_answer,
            f"<input>{json.dumps(dialogues[key], ensure_ascii=False, indent=2)}</input>",
        )
        logging.info(str(data.usage))
        logging.info(str(data.content[0].text))
        print(prompt)
        with open(f"./works/{key}.txt", mode="w", encoding="utf-8") as f:
            try:
                # TODO get json from data content from xml
                result = json.loads(data.content[0].text.replace("<result>", "").replace("</result>", ""))
                f.write(json.dumps(result, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                logging.error(f"{key} JSONDecodeError")
                f.write(repr(data.content[0].text))


def process_key(claude, prompt, first_answer, key):
    if os.path.exists(f"./works/{key}.txt"):
        logging.info(f"{key} already exists")
        return key, False  # 파일이 이미 존재하므로 처리하지 않음
    logging.info(f"Processing {key}")
    try:
        logging.info(json.dumps(dialogues[key], ensure_ascii=False))
        data = claude.translate(
            prompt,
            first_answer,
            f"<input>{json.dumps(dialogues[key], ensure_ascii=False, indent=2)}</input>",
        )
        result = json.loads(data.content[0].text.replace("<result>", "").replace("</result>", ""))
        logging.info(str(data.usage))
        logging.info(str(data.content[0].text))
        with open(f"./works/{key}.txt", mode="w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return key, True  # 성공적으로 처리됨
    except Exception as e:
        with open(f"./works/{key}.txt", mode="w", encoding="utf-8") as f:
            f.write(repr(data.content[0].text))
        logging.error(f"Error processing {key}: {e}")
        return key, False  # 처리 중 오류 발생


def batch_process_concurrent(start_index=0, end_index=None, max_workers=5):
    if end_index is None:
        end_index = len(dialogue_keys)

    prompt = "당신의 임무는 중국에서 제작된 무협 RPG 게임 \"천명기어\"를 무협 세계관을 유지하면서 한국어로 번역하는 것입니다.\n번역 지침:\n\n말투 구분\n\n존댓말: 부탁이나 공경의 표현에 사용. 예: \"謹聽莊主之命！\" → \"장주님의 명에 따르겠습니다.\"\n반말: 도발적, 협박적, 고압적인 말투에 사용. 예: \"軟柿子，受死吧！\" → \"나약한 놈, 죽어라!\"\n평서체: 불확실한 상황이나 상황 설명에 사용. 예: \"夾層中放了一張紙，寫著「揚瀾小鎮怪郎中」。\" → \"사이에 끼워진 종이에는, '양란소진괴랑중(揚瀾小鎮怪郎中)'이 적혀있다.\"\n\n\n태그와 플레이스홀더 유지\n\n\"{}\"안의 내용 유지. 예: \"這是{it2000_03}。\" → \"이것은 {it2000_03}이다.\"\n\"<>\"안의 내용 유지. 예: \"這<color=#FF0000>茶葉</color>你就拿去吧！\" → \"이 <color=#FF0000>찻잎</color>을 가져가!\"\n\n\n무협 세계관 유지\n\n영어에서 유래한 외래어 대신 한글/한자어 사용. 예: \"一掌\" → \"일장\", \"桌子\" → \"탁자\"\n무협식 호칭 주의. 예: \"大俠\" → \"대협\", \"師兄\" → \"사형\", \"師姐\" → \"사저\"\n\n\n한자 병기\n\n이름, 지명, 무공, 물건, 별명에 적용. 예: \"柴玉關\" → \"시옥관(柴玉關)\"\n고사성어는 뜻도 병기. 예: \"<color=#FF0000>果老騎驢</color>\" → \"<color=#FF0000>과로기려(果老騎驢:당나귀를 거꾸로 탄 노f인)</color>\"\n\n\n애칭 표현 주의\n\n\"小\"글자로 시작하는 이름은 애칭으로 처리. 예: \"小玥\" → \"소월\", \"小梅\" → \"소매\"\n\"小子\"는 상황에 따라 \"꼬맹이\" 또는 \"애송이\" 등으로 번역\n\n\n메타데이터 활용\n\n제공된 메타데이터의 용어를 우선적으로 사용하여 일관성 있는 번역 유지\n\n\n\n입력 데이터 형식:\n<input>\n{\n\"need_translate\": {\n\"1104904601\": \"중국어 텍스트\",\n\"1104904602\": \"중국어 텍스트\",\n\"1104904603\": \"중국어 텍스트\"\n},\n\"meta_data\": {\n\"용어1\": \"번역1\",\n\"용어2\": \"번역2\"\n}\n}\n</input>\n응답은 다음 <result> 태그 내에 json 형식으로 제공하세요:\n<result>\n{\n\"1104904601\": \"번역 결과\",\n\"1104904602\": \"번역 결과\",\n\"1104904603\": \"번역 결과\"\n}\n</result>"
    first_answer = "네, 이해했습니다. 중국어 무협 RPG 게임 \"천명기어\"의 텍스트를 한국어로 번역하되, 무협 세계관을 유지하고 자연스러운 한국어로 옮기겠습니다. 특수 태그와 알파벳, 숫자는 그대로 유지하고, 대화 상황에 맞는 말투를 사용하며 현대적 용어는 피하겠습니다. 제공된 meta_data가 있다면 참고하여 번역하겠습니다. 번역 결과는 요청하신 JSON 형식으로 제공하겠습니다. 중국어 텍스트를 입력해 주시면 번역을 시작하겠습니다."
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    claude = Claude3Api(api_key)

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for key in dialogue_keys[start_index:end_index]:
            future = executor.submit(process_key, claude, prompt, first_answer, key)
            futures.append(future)

        # 진행 상황을 표시하기 위해 tqdm을 사용
        for future in tqdm.tqdm(
            concurrent.futures.as_completed(futures), total=len(futures)
        ):
            key, success = future.result()
            if success:
                logging.info(f"Successfully processed {key}")
            else:
                logging.error(f"Failed to process {key}")


if __name__ == "__main__":
    api_key = toml.load("localconfig.toml")["local"]["CLAUDE_API_KEY"]
    logging.basicConfig(
        level=logging.INFO,
        filename="translator.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )
    # test_function()
    # test_function2(api_key)
    # dialogues = json.load(
    #     open("./data/sliced_texts.json", mode="r", encoding="utf-8")
    # )
    # batch_process_concurrent(0, None , max_workers=10)
    dialogues = json.load(
        open("./untranslated_with_meta_data.json", mode="r", encoding="utf-8")
    )
    batch_process_concurrent(0, None , max_workers=10)
    # batch_process_concurrent(dialogue_keys.index("TNPC_30043301#0"),dialogue_keys.index("TNPC_30043301#0")+1, max_workers=1)