import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

training_data = [
    # ── GREETINGS ─────────────────────────────────────────────────
    ('e kaaro', 'greeting'), ('e kaasan', 'greeting'), ('e kaale', 'greeting'),
    ('bawo ni', 'greeting'), ('bawo lo se wa', 'greeting'), ('o daro', 'greeting'),
    ('o daaro', 'greeting'), ('e jowo', 'greeting'), ('pele o', 'greeting'),
    ('se o gbo mi', 'greeting'), ('soro didie', 'greeting'), ('jowo tun wi', 'greeting'),
    ('mi o gbo e', 'greeting'), ('se o ye o', 'greeting'), ('mo fe soro', 'greeting'),
    ('e je ki a soro', 'greeting'), ('bawo ni ojo re', 'greeting'),
    ('o ti ji', 'greeting'), ('orun rere', 'greeting'), ('mo sun daadaa', 'greeting'),
    ('mo re', 'greeting'), ('kii se isoro', 'greeting'), ('o dara', 'greeting'),
    ('o dara pupo', 'greeting'), ('e je ki a bere', 'greeting'),
    ('mo ti pari', 'greeting'), ('duro die', 'greeting'), ('hello', 'greeting'),
    ('hi', 'greeting'), ('kaabo', 'greeting'), ('nle o', 'greeting'),
    ('se alaafia ni', 'greeting'), ('good morning', 'greeting'),
    ('good afternoon', 'greeting'), ('good evening', 'greeting'),

    # ── NAME ──────────────────────────────────────────────────────
    ('ki ni oruko re', 'name'), ('ta ni o', 'name'), ('oruko re ni kini', 'name'),
    ('se robot ni e', 'name'), ('tani oluranlowo', 'name'), ('ki ni e npe e', 'name'),
    ('nibo ni iwo wa', 'name'), ('ta ni iwo', 'name'), ('who are you', 'name'),
    ('what is your name', 'name'),

    # ── SELF INTRO ────────────────────────────────────────────────
    ('mo je iranlowo re', 'self_intro'),
    ('oruko mi ni iranlo wo yoruba', 'self_intro'),
    ('mo wa nibi lati ran e lowo', 'self_intro'),
    ('emi ni oluranlowo yoruba re', 'self_intro'),
    ('bawo ni mo se le ran e lowo', 'self_intro'),
    ('introduce yourself', 'self_intro'),
    ('tell me about yourself', 'self_intro'),

    # ── WHAT CAN YOU DO ───────────────────────────────────────────
    ('kini o le se', 'what_can_you_do'), ('kini ise re', 'what_can_you_do'),
    ('ise wo ni o le se', 'what_can_you_do'), ('ran mi lowo pelu kini', 'what_can_you_do'),
    ('se o le ran mi lowo', 'what_can_you_do'), ('kini awon ishe re', 'what_can_you_do'),
    ('kini iwo le se fun mi', 'what_can_you_do'), ('what can you do', 'what_can_you_do'),
    ('what are your abilities', 'what_can_you_do'),

    # ── THANKS ────────────────────────────────────────────────────
    ('e seun', 'thanks'), ('o seun', 'thanks'), ('ese pupo', 'thanks'),
    ('e dupe', 'thanks'), ('dupe lowo re', 'thanks'), ('ko to nkan', 'thanks'),
    ('o dara', 'thanks'), ('daadaa', 'thanks'), ('mo dupẹ', 'thanks'),
    ('thank you', 'thanks'), ('thanks', 'thanks'), ('well done', 'thanks'),

    # ── APOLOGY ───────────────────────────────────────────────────
    ('e pele', 'apology'), ('e ma binu', 'apology'), ('sorry', 'apology'),
    ('e je ki a tun gbiyanju', 'apology'), ('e tun so', 'apology'),
    ('forgive me', 'apology'), ('i am sorry', 'apology'),

    # ── CONFIRM ───────────────────────────────────────────────────
    ('beeni', 'confirm'), ('yes', 'confirm'), ('mo gba', 'confirm'),
    ('se e', 'confirm'), ('oya se', 'confirm'), ('proceed', 'confirm'),
    ('go ahead', 'confirm'), ('ok', 'confirm'), ('alright', 'confirm'),

    # ── CANCEL ────────────────────────────────────────────────────
    ('rara', 'cancel'), ('no', 'cancel'), ('ma se', 'cancel'),
    ('fi sile', 'cancel'), ('da duro', 'cancel'), ('cancel', 'cancel'),
    ('stop it', 'cancel'), ('never mind', 'cancel'),

    # ── EXIT ──────────────────────────────────────────────────────
    ('jade', 'exit'), ('odabo', 'exit'), ('bye', 'exit'),
    ('fi mi sile', 'exit'), ('pari', 'exit'), ('da duro', 'exit'),
    ('o dabo', 'exit'), ('jade kuro', 'exit'), ('goodbye', 'exit'),
    ('close app', 'exit'), ('quit', 'exit'),

    # ── HELP ──────────────────────────────────────────────────────
    ('ran mi lowo', 'help'), ('mo nilo iranlowo', 'help'),
    ('ejo e gba mi lowo', 'help'), ('mo ni ibeere', 'help'),
    ('mo padanu', 'help'), ('e ran mi lowo', 'help'),
    ('kini isoro', 'help'), ('mo ni isoro', 'help'), ('kini ojutu', 'help'),
    ('help me', 'help'), ('i need help', 'help'),

    # ── TIME ──────────────────────────────────────────────────────
    ('ago melo ni', 'time'), ('akoko melo ni oni', 'time'),
    ('melo ni aago bayi', 'time'), ('se o le so akoko fun mi', 'time'),
    ('kini akoko', 'time'), ('igba melo ni', 'time'),
    ('kini ago', 'time'), ('so akoko fun mi', 'time'),
    ('ki ni akoko bayi', 'time'), ('what time is it', 'time'),
    ('current time', 'time'), ('what time', 'time'),

    # ── DATE ──────────────────────────────────────────────────────
    ('ojo wo ni oni', 'date'), ('ojo wo ni ola', 'date'),
    ('osu wo ni bayi', 'date'), ('kini ojo oni', 'date'),
    ('ojo melo ni osu yi', 'date'), ('kini ojo ola', 'date'),
    ('kini ojo ana', 'date'), ('so ojo oni', 'date'),
    ('ki ni date oni', 'date'), ('what day is today', 'date'),
    ('today date', 'date'), ('current date', 'date'),

    # ── WEATHER ───────────────────────────────────────────────────
    ('bawo ni ojo ojo', 'weather'), ('se ojo ma ro loni', 'weather'),
    ('iwon otutu melo ni loni', 'weather'), ('bawo ni ojo ojo ola', 'weather'),
    ('se ojo n ro bayi', 'weather'), ('kini ipo ojo ojo', 'weather'),
    ('bawo ni ojo ojo ni eko', 'weather'), ('kini ojo loni', 'weather'),
    ('se ojo yoo ro', 'weather'), ('iwo otutu', 'weather'),
    ('what is the weather', 'weather'), ('weather today', 'weather'),

    # ── OPEN APPS ─────────────────────────────────────────────────
    ('sii chrome', 'chrome'), ('mo fe chrome', 'chrome'), ('gbe chrome soke', 'chrome'),
    ('tan chrome', 'chrome'), ('open chrome', 'chrome'), ('si chrome', 'chrome'),

    ('sii browser', 'browser'), ('sii asawakiri', 'browser'), ('mo fe browser', 'browser'),
    ('open browser', 'browser'), ('web browser', 'browser'),

    ('sii notepad', 'notepad'), ('mo fe notepad', 'notepad'), ('tan notepad', 'notepad'),
    ('open notepad', 'notepad'), ('si notepad', 'notepad'),

    ('sii calculator', 'calculator'), ('mo fe calculator', 'calculator'),
    ('tan calculator', 'calculator'), ('sii isiro', 'calculator'),
    ('open calculator', 'calculator'), ('si isiro', 'calculator'),

    ('sii settings', 'settings'), ('mo fe settings', 'settings'),
    ('sii eto', 'settings'), ('sii windows settings', 'settings'),
    ('tan settings', 'settings'), ('open settings', 'settings'), ('si eto', 'settings'),

    ('sii explorer', 'explorer'), ('sii faili explorer', 'explorer'),
    ('mo fe explorer', 'explorer'), ('sii faili', 'explorer'),
    ('open file explorer', 'explorer'), ('si faili', 'explorer'),

    ('sii vscode', 'vscode'), ('sii visual studio code', 'vscode'),
    ('mo fe vscode', 'vscode'), ('gbe vscode soke', 'vscode'),
    ('open vscode', 'vscode'), ('tan vscode', 'vscode'), ('si vscode', 'vscode'),

    ('sii word', 'word'), ('mo fe word', 'word'), ('sii microsoft word', 'word'),
    ('open word', 'word'), ('si word', 'word'), ('tan word', 'word'),

    ('sii excel', 'excel'), ('mo fe excel', 'excel'), ('gbe excel soke', 'excel'),
    ('tan excel', 'excel'), ('sii microsoft excel', 'excel'),
    ('open excel', 'excel'), ('si excel', 'excel'),

    ('sii powerpoint', 'powerpoint'), ('mo fe powerpoint', 'powerpoint'),
    ('tan powerpoint', 'powerpoint'), ('sii microsoft powerpoint', 'powerpoint'),
    ('open powerpoint', 'powerpoint'), ('si powerpoint', 'powerpoint'),

    ('sii cmd', 'cmd'), ('sii command prompt', 'cmd'), ('mo fe cmd', 'cmd'),
    ('open cmd', 'cmd'), ('command line', 'cmd'),

    ('sii powershell', 'powershell'), ('mo fe powershell', 'powershell'),
    ('gbe powershell soke', 'powershell'), ('open powershell', 'powershell'),

    ('sii task manager', 'taskmanager'), ('mo fe task manager', 'taskmanager'),
    ('tan task manager', 'taskmanager'), ('open task manager', 'taskmanager'),
    ('si task manager', 'taskmanager'),

    ('sii whatsapp', 'whatsapp'), ('mo fe whatsapp', 'whatsapp'),
    ('gbe whatsapp soke', 'whatsapp'), ('open whatsapp', 'whatsapp'),
    ('si whatsapp', 'whatsapp'),

    ('sii microsoft store', 'store'), ('si store', 'store'),
    ('mo fe store', 'store'), ('open store', 'store'), ('sii store', 'store'),

    ('sii kamera', 'camera'), ('si kamera', 'camera'), ('mo fe kamera', 'camera'),
    ('tan kamera', 'camera'), ('open camera', 'camera'),

    ('sii git bash', 'gitbash'), ('mo fe git bash', 'gitbash'),
    ('gbe git bash soke', 'gitbash'), ('sii terminal', 'gitbash'),

    # ── CLOSE APPS ────────────────────────────────────────────────
    ('pa chrome', 'close_chrome'), ('da chrome duro', 'close_chrome'),
    ('close chrome', 'close_chrome'), ('fi chrome sile', 'close_chrome'),
    ('pa google chrome', 'close_chrome'),

    ('pa word', 'close_word'), ('da word duro', 'close_word'),
    ('close word', 'close_word'), ('fi word sile', 'close_word'),
    ('pa microsoft word', 'close_word'),

    ('pa excel', 'close_excel'), ('da excel duro', 'close_excel'),
    ('close excel', 'close_excel'), ('fi excel sile', 'close_excel'),
    ('pa microsoft excel', 'close_excel'),

    ('pa notepad', 'close_notepad'), ('da notepad duro', 'close_notepad'),
    ('close notepad', 'close_notepad'), ('fi notepad sile', 'close_notepad'),

    ('pa calculator', 'close_calculator'), ('da calculator duro', 'close_calculator'),
    ('close calculator', 'close_calculator'), ('fi calculator sile', 'close_calculator'),

    ('pa whatsapp', 'close_whatsapp'), ('da whatsapp duro', 'close_whatsapp'),
    ('close whatsapp', 'close_whatsapp'), ('fi whatsapp sile', 'close_whatsapp'),

    ('pa app yii', 'close_app'), ('da app duro', 'close_app'),
    ('close this app', 'close_app'), ('jade kuro ninu app', 'close_app'),
    ('pa ohun ti o sii', 'close_app'), ('close app', 'close_app'),

    # ── CLOSE TAB ─────────────────────────────────────────────────
    ('pa taabu yii', 'close_tab'), ('close this tab', 'close_tab'),
    ('close tab', 'close_tab'), ('pa tab yii', 'close_tab'),
    ('da taabu duro', 'close_tab'),

    # ── VOLUME ────────────────────────────────────────────────────
    ('gbe ohun soke', 'volume_up'), ('gbe volume soke', 'volume_up'),
    ('mu ohun ga', 'volume_up'), ('soke', 'volume_up'), ('louder', 'volume_up'),
    ('increase volume', 'volume_up'), ('volume up', 'volume_up'),

    ('din ohun ku', 'volume_down'), ('gbe volume wale', 'volume_down'),
    ('gbe ohun wale', 'volume_down'), ('dinku ohun', 'volume_down'),
    ('wale', 'volume_down'), ('quieter', 'volume_down'),
    ('decrease volume', 'volume_down'), ('volume down', 'volume_down'),

    ('pa ohun', 'mute'), ('dake', 'mute'), ('mu ohun dake', 'mute'),
    ('mute', 'mute'), ('silence', 'mute'), ('pa ohun run', 'mute'),

    # ── BRIGHTNESS ────────────────────────────────────────────────
    ('gbe imole soke', 'brightness_up'), ('mu imole ga', 'brightness_up'),
    ('increase brightness', 'brightness_up'), ('imole soke', 'brightness_up'),
    ('brighter', 'brightness_up'),

    ('gbe imole wale', 'brightness_down'), ('dinku imole', 'brightness_down'),
    ('decrease brightness', 'brightness_down'), ('imole wale', 'brightness_down'),
    ('dimmer', 'brightness_down'), ('din imole ku', 'brightness_down'),

    # ── WIFI ──────────────────────────────────────────────────────
    ('tan wifi', 'wifi_on'), ('mu wifi soke', 'wifi_on'),
    ('fi wifi sii', 'wifi_on'), ('turn on wifi', 'wifi_on'), ('enable wifi', 'wifi_on'),

    ('pa wifi', 'wifi_off'), ('da wifi duro', 'wifi_off'),
    ('pa wifi run', 'wifi_off'), ('turn off wifi', 'wifi_off'),
    ('disable wifi', 'wifi_off'),

    # ── BLUETOOTH ─────────────────────────────────────────────────
    ('tan bluetooth', 'bluetooth_on'), ('mu bluetooth soke', 'bluetooth_on'),
    ('fi bluetooth sii', 'bluetooth_on'), ('turn on bluetooth', 'bluetooth_on'),
    ('enable bluetooth', 'bluetooth_on'),

    ('pa bluetooth', 'bluetooth_off'), ('da bluetooth duro', 'bluetooth_off'),
    ('turn off bluetooth', 'bluetooth_off'), ('disable bluetooth', 'bluetooth_off'),
    ('pa bluetooth run', 'bluetooth_off'),

    # ── SCREENSHOT ────────────────────────────────────────────────
    ('se igbasile iboju', 'screenshot'), ('ya aworan iboju', 'screenshot'),
    ('ya foto iboju', 'screenshot'), ('ya screenshot', 'screenshot'),
    ('se screenshot', 'screenshot'), ('take screenshot', 'screenshot'),
    ('capture screen', 'screenshot'),

    # ── LOCK / SLEEP / SHUTDOWN / RESTART ─────────────────────────
    ('di komputa mo', 'lock'), ('tiipa komputa', 'lock'),
    ('lock screen', 'lock'), ('pa iboju', 'lock'), ('tiipa iboju', 'lock'),

    ('sun', 'sleep'), ('pa iboju run', 'sleep'), ('se sleep', 'sleep'),
    ('hibernate', 'sleep'), ('sleep computer', 'sleep'),

    ('tun bere komputa', 'restart'), ('restart komputa', 'restart'),
    ('reboot', 'restart'), ('start again', 'restart'), ('restart', 'restart'),
    ('bere leẹkansi', 'restart'),

    ('pa komputa', 'shutdown'), ('di komputa pa', 'shutdown'),
    ('turn off computer', 'shutdown'), ('shutdown', 'shutdown'),
    ('power off', 'shutdown'), ('pa ero', 'shutdown'),

    # ── SYSTEM INFO ───────────────────────────────────────────────
    ('bawo ni batiri mi se wa', 'battery'), ('kini ipele batiri mi', 'battery'),
    ('battery level', 'battery'), ('check battery', 'battery'),
    ('batiri melo ni mo ku', 'battery'), ('how much battery', 'battery'),

    ('bawo ni ipamo mi se wa', 'storage'), ('kini aaye ti o ku ninu komputa', 'storage'),
    ('check storage', 'storage'), ('how much storage', 'storage'),
    ('ipamo melo ni o ku', 'storage'), ('disk space', 'storage'),

    ('bawo ni memory mi se wa', 'ram'), ('kini ipele ram mi', 'ram'),
    ('check ram', 'ram'), ('how much ram', 'ram'),
    ('ram melo ni mo lo', 'ram'), ('memory usage', 'ram'),

    ('bawo ni processor mi se wa', 'cpu'), ('kini ipele cpu mi', 'cpu'),
    ('check cpu', 'cpu'), ('cpu usage', 'cpu'),
    ('processor melo ni mo lo', 'cpu'), ('check processor', 'cpu'),

    # ── SEARCH & BROWSER ──────────────────────────────────────────
    ('wa nkan fun mi', 'search'), ('wa lori google', 'search'),
    ('search for', 'search'), ('google it', 'search'),
    ('wa lori intanẹẹti', 'search'), ('wa fun mi', 'search'),
    ('find', 'search'), ('look up', 'search'),

    ('wa lori youtube', 'search_youtube'), ('search on youtube', 'search_youtube'),
    ('youtube', 'search_youtube'), ('wa fideo lori youtube', 'search_youtube'),
    ('se wiwa lori youtube', 'search_youtube'),

    ('sii taabu titun', 'new_tab'), ('open new tab', 'new_tab'),
    ('new tab', 'new_tab'), ('taabu titun', 'new_tab'), ('sii tab titun', 'new_tab'),

    ('pada sehin', 'go_back'), ('go back', 'go_back'),
    ('back', 'go_back'), ('pada', 'go_back'), ('lo sehin', 'go_back'),

    ('tun gbe', 'refresh'), ('refresh', 'refresh'),
    ('reload', 'refresh'), ('tun load', 'refresh'), ('tun se', 'refresh'),

    # ── MUSIC & MEDIA ─────────────────────────────────────────────
    ('tan music', 'music'), ('tan orin', 'music'), ('mu orin wa', 'music'),
    ('play music', 'music'), ('sii spotify', 'music'), ('se orin', 'music'),
    ('sii orin', 'music'), ('mo fe orin', 'music'), ('orin yoruba', 'music'),
    ('orin fuji', 'music'), ('orin juju', 'music'),

    ('da orin duro', 'pause_music'), ('pause music', 'pause_music'),
    ('pause', 'pause_music'), ('duro', 'pause_music'),
    ('da orin duro fun igba die', 'pause_music'),

    ('orin to tele', 'next_song'), ('next song', 'next_song'),
    ('skip song', 'next_song'), ('gbe orin to tele', 'next_song'),
    ('next', 'next_song'),

    ('orin ti o koja', 'prev_song'), ('previous song', 'prev_song'),
    ('go back song', 'prev_song'), ('orin sehin', 'prev_song'),
    ('previous', 'prev_song'),

    # ── CALENDAR / EMAIL ──────────────────────────────────────────
    ('sii calendar', 'calendar'), ('seto isele titun', 'calendar'),
    ('sii imeeli', 'email'), ('ko imeeli titun', 'email'),
    ('firansey imeeli', 'email'),

    # ── SMART HOME ────────────────────────────────────────────────
    ('tan fitila', 'smart_home'), ('pa fitila', 'smart_home'),
    ('tan afefe', 'smart_home'), ('pa afefe', 'smart_home'),
    ('tan ac', 'smart_home'), ('pa ac', 'smart_home'),
    ('gbe tv soke', 'smart_home'), ('pa tv', 'smart_home'),

    # ── MATH ──────────────────────────────────────────────────────
    ('kini ookan afikun ookan', 'calculator'), ('se isiro fun mi', 'calculator'),
    ('kini square root', 'calculator'), ('kini iye owo', 'calculator'),
    ('calculate', 'calculator'), ('math', 'calculator'),

    # ── LEARNING ──────────────────────────────────────────────────
    ('kini oro yoruba fun', 'learn'), ('ko mi ni yoruba', 'learn'),
    ('kini itan ile ife', 'learn'), ('kini python', 'learn'),
    ('kini ai', 'learn'), ('kini machine learning', 'learn'),

    # ── ALARM / REMINDER ──────────────────────────────────────────
    ('se o le ji mi ni ago mefa', 'alarm'), ('pa alarinrin', 'alarm'),
    ('seto alarinrin fun ola', 'alarm'), ('kini alarinrin mi', 'alarm'),
    ('ranti mi mu oogun', 'reminder'), ('ranti mi se idaraya', 'reminder'),
]

texts   = [d[0] for d in training_data]
intents = [d[1] for d in training_data]

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))),
    ('clf',   LogisticRegression(max_iter=2000, C=5)),
])

pipeline.fit(texts, intents)
joblib.dump(pipeline, 'models/intent_model.pkl')

print('Intent model retrained!')
print(f'Total examples : {len(texts)}')
print(f'Unique intents : {len(set(intents))}')
print()
print('Intents:')
for intent in sorted(set(intents)):
    count = intents.count(intent)
    print(f'  {intent:<20} {count} examples')
