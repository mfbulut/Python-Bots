import praw
import time
import random

quotes = [
    "Kalbimi ve ruhumu vermemin bir yararı yok, sen zaten bunlara sahipsin. O yüzden sana bir ayna getirdim. Kendine bak beni hatırla.",
    "Güzelliğin bir damlası olan Leyla için uykuyu haram etmek çok değilse, güzelliğin kaynağı Mevla için bir ömrü feda etmek az bile.",
    "Başta dönüp koşan nice bilgiler, nice hünerler vardır ki, insan onunla baş olmak isterse, baş elden gider. Başının gitmesini istemiyorsan ayak ol.",
    "Kalbin bir gün seni sevgiliye götürecek. Ruhun bir gün seni sevgiliye taşıyacak. Sakın acında kaybolma. Bil ki çektiğin acı bir gün dermanın olacak.",
    "Nefsin ejderhadır. Öldü sanma, uykuya dalar o. Dertten eline fırsat düşmediği için uyur. Derdin bitince çıkar hemen. Hüner; dertsizken de nefsi uykuda tutmadadır.",
    "Her zorluğun sonunda doğan bir ışık vardır. Eğer elleriniz diken yaralarıyla kan revan içinde kaldıysa güle dokunmanıza çok az kalmış demektir.",
    "Yaşadığın dünyaya bak; yüce tanrı, hangi eserini sevginin kucağında büyütmemiş? Neden okşamak ve kucaklamakla gidilecek yere, tekme ve tokatla erişmeyi tercih edesin?",
    "Küle döndüysen, yeniden güle dönmeyi bekle. Ve geçmişte kaç kere küle dönüştüğünü değil, kaç kere yeniden küllerin arasından doğrulup yeni bir gül olduğunu hatırla.",
    "Sarılmayı bilir misin? Sahiplenmeyi, sahiplendiğinde sadık kalmayı? Sen bilir misin aşık olmayı? Bölünebilir misin ikilere, üçlere, gerekirse binlere? Yapabilir misin? Gerçekten sevebilir misin? Sevmenin demesi olmaz. Unutma; ya çok seversin bir kere, ya da hiç sevmezsin.",
    "Ey sevgili; heyben acıyla dolar da nefes alamazsan gel. Huzur bulacağın kıyılarım senindir. Umutların solar kurur da su bulamazsan beraber sulayalım, gözyaşlarım senindir. Kanadın kırılır da maviye uçamazsan, ne güne duruyor al, kanatlarım senindir. Çaresiz çilelere bir umut bulamazsan, kendime ettiğim dualarım senindir.",
    "Gönül almayı bilmeyene ömür emanet edilmez.",
    "Seni bağrıma değil, bağrımı ve başımı ayağının altına bastım. Gözüm toprak olacak, ama gönlüm daima aşk kokacak.",
    "Her yerde olmak gibi bir duan varsa, gönüllere gir; çünkü sevenler, sevdiklerini gönüllerinde taşırlar.",
    "Ay doğmuyorsa yüzüne, güneş vurmuyorsa pencerene, kabahati ne güneşte ne de ay da ara! Gözlerindeki perdeyi arala!",
    "Ey sevgili. Biz seninle bir salkımın iki aşık üzümüyken, başka şişelerde şarap olmuşuz, başka hayallerde harap olmuşuz.",
    "İyiyim desem yalan olur, kötüyüm desem inancıma dokunur. En iyisi şükre vurayım dilimi, belki o zaman kalbim kurtulur.",
    "Altın ne oluyor, can ne oluyor, inci, mercan da nedir bir sevgiye harcanmadıktan, bir sevgiliye feda edilmedikten sonra.",
    "Şarap küpü nereye konursa konsun şaraptır. Gül mezbelelikte bitmekle kötü olmaz, şarap altın tasa konmakla helal olmaz.",
    "Merhamette güneş gibi ol; cömertlikte akarsu gibi ol; tevazuda toprak gibi ol; ayıpları, kusurları örtmekte gece gibi ol.",
    "Misafirsin bu hanede ey gönül, umduğunla değil bulduğunla gül, hane sahibi ne derse o olur, ne kimseye sitem eyle, ne üzül.",
    "Aşk nasip işidir hesap işi değil! Aşk adayıştır arayış değil! Sen adanmışsan ve yanmışsan bu uğurda aşk seni bulmaya gelir.",
    "Aradığın seni arayandır.",
    "Nefsin, üzüm ve hurma gibi tatlı şeylerin sarhoşu oldukça, ruhunun üzüm salkımını görebilir misin ki?",
    "Yılan sokması seni sadece canından eder. Ama kötü dost hem candan, hem de imandan eder!",
    "Aklım her gün tövbe eder. Nefsim her an tövbemi bozar. Arada kalmış bîçareyim. İyi ki senin kapın var.",
    "Dediler ki: gözden ırak olan gönülden de ırak olur. Dedim ki: gönle giren gözden ırak olsa ne olur.",
    "Beni çok özle, bir daha bu kadar sevmeyecekler seni. Aşksız olma ki ölü olmayasın. Aşkta öl ki diri kalasın.",
    "Nasibinde varsa alırsın karıncadan bile ders. Nasibinde yoksa bütün cihan önüne serilse sana ters.",
    "Yürürken başımın yerde olması sizi rahatsız etmesin. Benim tek derdim; yere düşen edebinize takılmamak.",
    "Sen çiçek olup etrafa gülücükler saçmaya söz ver. Toprak olup seni başının üstünde taşıyan bulunur.",
    "Ey sahura kalkan, sahur yemeği yiyen kişi! Az konuş, hatta sus! Sus da orucu anlayanlar, oruçtan söz etsinler.",
    "Kimle gezdiğinize, kimle arkadaşlık ettiğinize dikkat edin. Çünkü bülbül güle, karga çöplüğe götürür.",
    "Gerek yok her sözü laf ile beyana. Bir bakış bin söz eder, bakıştan anlayana.",
    "Bir muammadır aşk. Kiminin vicdanına atılan taş, kiminin de gözünden akıtılan yaştır aşk.",
    "Gel de birbirimizin kadrini bilelim. Çünkü ansızın ayrılacağız birbirimizden.",
    "Küsmek ve darılmak için bahaneler aramak yerine, sevmek ve sevilmek için çareler arayın.",
    "Yüz kişinin içinde aşık, gökte yıldızlar arasında parıldayan ay gibi belli olur.",
    "Bir yandan korkun bir yandan umudun varsa iki kanatlı olursun. Tek kanatla uçulmaz zaten.",
    "Muhabbet ve merhamet, insanlığın; hiddet ve şehvet de hayvanların sıfatlarıdır.",
    "Ey Müslüman, edep nedir diye sorarsan bil ki edep, her edepsizin edepsizliğine katlanmaktır.",
    "Akıl bir kuzu, nefis bir kurt, iman ise çobandır. İman kuvvetli olmazsa, nefis aklı yer.",
    "Aşkın hikâyesini, durmaksızın feryâd eden bülbüle değil. Sessiz sedasız can veren pervanelere sor.",
    "Sus gönlüm! Bütün bu susmalarına karşılık her şeyin hayırlısının olacağına inanarak sus.",
    "Birini tanımadıysan kimin ve neyin peşinde olduğuna bak! Anlarsın…",
    "Bir gönülde aşk ve sevgi ateşi yoksa o kişi karanlıklarda, Allah nurundan habersizdir.",
    "İsyanlardayım dedi. Hayır, imtihanlardaydı. Fark etseydi, kurtulacaktı.",
    "Öyle bir ‘yâr’ sev ki evladım; elinde su tasıyla, iftarı bekleyen oruçlu gibi beklesin seni.",
    "Toprak gibi sessiz olduğum an bil ki; şimşek gibi gökte gürlüyor feryadım.",
    "Tut ki Ali’den sana miras kaldı Zülfikar. Sende Ali’nin yüreği yoksa Zülfikar neye yarar?",
    "Kalbi ve sözü bir olmayan kimsenin yüz dili bile olsa, o yine dilsiz sayılır.",
    "Dilini terbiye etmeden önce yüreğini terbiye et; çünkü söz yürekten gelir, dilden çıkar.",
    "Ben hiç dilek tutmadım, hep dua ettim. Ömrün ömrüme nasip olsun diye!",
    "Kapı açılır, sen yeter ki vurmayı bil! Ne zaman? Bilemem! Yeter ki o kapıda durmayı bil!",
    "Ne kadar bilirsen bil, söylediklerin karşındakilerin anlayabileceği kadardır.",
    "Birini tanımadıysan kimin ve neyin peşinde olduğuna bak! Anlarsın…",
    "Cahille girme münakaşaya. Ya sinirini zıplatır tavana! Ya da yazık olur adabına.",
    "Kim, ne olursa olsun, sevgili bizim olsun tek, canı, canımız olsun.",
    "Kötülük yaptın mı kork! Çünkü o bir tohumdur. Allah yeşertir, karşına çıkarır.",
    "Aynı dili konuşanlar değil, aynı duyguları paylaşanlar anlaşabilir.",
    "Gülü gülene ver. Kalbini sevene ver. Sevmek güzel şeydir. Kıymet bilene ver.",
    "Can’ı Canan’a teslime hazır değilsen ‘ben Aşk’ım’ deme kimseye.",
    "İmtihan içinde imtihan vardır. Derlen toparlan da ufak bir imtihana satma kendini.",
    "Şikayetçi, kötü huyludur. İyi huylu şikayet etmez, tahammül eder.",
    "Gözyaşının bile görevi varmış. Ardından gelecek gülümseme için temizlik yaparmış.",
    "Üç sözden fazla değil, tüm ömrüm şu üç söz; hamdım, piştim, yandım.",
    "Yok, dünyada hicrandan daha acı ne istiyorsan et de onu etme.",
    "Kitaplardan önce, kendimizi okumaya çalışalım.",
    "Kanat vardır doğanı padişaha götürür; kanat vardır kuzgunu leşe götürür.",
    "Ey dost! Derdin ne olursa olsun umudun her zaman Allah olsun.",
    "Bazen halimize Melekler imrenir. Bazen de halimizden Şeytan bile iğrenir.",
    "Susmak, mana eksikliğinden değil. Belki mana derinliğindendir.",
    "Kır oğul zinciri; hür gez, hür konuş, yok mu altından gümüşten bir kurtuluş?",
    "Yapraksız kaldın diye gövdeni kestirme. Zira bu işin baharı var.",
    "Kim demiş gül yaşar dikenin himayesinde? Dikenin itibarı gül himayesinde!",
    "İnsan her şeyi göremez; sevdiğin şeyler, seni kör ve sağır eder.",
    "Cahil kişi gülün güzelliğini görmez, gider dikenine takılır.",
    "Bozuk olunca maya, ne ar tanır ne de hayâ!",
    "Gerçek aşk’ı bilen kalp bir damla suya bile hürmetle bakar.",
    "Bazı insanlar bize armağandır, bazıları ise ders.",
    "Çektirilen acı havada asılı kalmaz, çektirenin başına düşer.",
    "Sabır önceleri zehirdir. Huy edinirsen bal olur!",
    "Bir kimsede kibir varsa, söz söylediği zaman soğan gibi kokar.",
    "Gönül sevgiyi bulmuşsa kuru dal bile çiçek açar.",
    "Sen Allah’a güven. Hiç beklemediğin anda çiçek açar umutlar.",
    "Kalbinizle yaptığınız her şey size geri dönecektir.",
    "Harf’ler yetmedi anlaşılmama, bari hâl’den anla.",
    "Doğruların yemin etmeye ihtiyacı yoktur.",
    "Ahlak örtüsü olmayanı, başörtüsü dindar yapmaz.",
    "Dert, insanı yokluğa götüren rahvan attır.",
    "Okuyarak öğreneceksin ama severek anlayacaksın.",
    "Kimde bir güzellik varsa bilsin ki ödünçtür.",
    "Dua kapı çalmaktır. Gerisine karışmak haddi aşmaktır.",
    "Cahil kimsenin yanında kitap gibi sessiz ol.",
    "Köpeklerin kardeşliği, aralarına kemik atılana kadardır.",
    "Bilmez misin ki cevap vermemek de cevaptır.",
    "Gönül, gönül verilerek alınır.",
    "Gönül, ebedi olmayan mülkü, bir rüya bil!",
    "Kusur arıyorsan, tüm aynalar senin.",
    "Kaderde sevmek var ama kavuşmak yok ise şayet, olsun! Vuslata aşık gönül susmaya da razı.",
    "Ne zaman gökyüzüne bir nefes, bir dua gönderdin de ardınca ona benzer iyilik görmedin?",
    "Köpeklerin kardeşliği, aralarına kemik atana kadardır.",
    "Dert, insanı yokluğa götüren rahvan attır.",
    "Kalp denizdir, dil de kıyı. Deniz de ne varsa kıyıya o vurur.",
    "Fakat harap olmaktan niye gamlanayım? Harabenin altında padişah hazinesi var.",
    "Aşk; sandığın kadar değil, yandığın kadardır...",
]

def login():
    print("Logging in...")
    # Fill here
    reddit = praw.Reddit(
        client_id="",
        client_secret="",
        user_agent="",
        username="",
        password="",
    )
    print("Logged in!")

    return reddit


def reply(p_type):

    print("Related words found in " + p_type.id)

    random_index = random.randint(0, len(quotes) - 1)

    p_type.reply(
        "Ben bir botum ve paylaşımında 'Mevlana' geçtiği için geldim. Senin için bir tane **Mevlana sözü** paylaştım:"
        + "\n\n"
        + quotes[random_index]
        + " \n\n "
        "*-Mevlânâ Celâleddîn-i Rûmî* \n\n "
        "^(I am a bot and this action was performed automatically.)"
    )

    print("Replied to " + p_type.id)


def main(reddit):

    subreddit = reddit.subreddit(
        "Semazenler+Turkey+TurkeyJerky+KGBTR+ArsivUnutmaz+AteistTurk+BLKGM+Turkmenistan+Otuken+MuslumanTurk+Tiele"
    )

    print("Collecting  last 5 mentions,last 200 comments and last 20 posts from new...")

    time.sleep(1)
    for mention in reddit.inbox.mentions(limit=5):
        if mention.new and mention.author != reddit.user.me():
            mention.mark_read()
            time.sleep(1)
            reply(mention)

    for submission in subreddit.new(limit=20):
        submission_lower = submission.title.lower()
        if submission.score >= 0:
            if (
                "mevlana" in submission_lower
                and submission.saved is False
                and submission.author != reddit.user.me()
            ):
                time.sleep(1)
                reply(submission)
                submission.save()

    for comment in subreddit.comments(limit=200):
        comment_lower = comment.body.lower()
        if comment.score >= 8:

            if (
                "mevlana" in comment_lower
                and comment.saved is False
                and comment.author != reddit.user.me()
            ):
                time.sleep(1)
                reply(comment)
                comment.save()

    print("Collect Completed.")

    print("Sleeping for 300 seconds...")
    time.sleep(300)


reddit = login()


while True:
    try:
        main(reddit)
    except Exception as e:
        print(str(e) + " ,sleeping 120 seconds...")
        time.sleep(120)
