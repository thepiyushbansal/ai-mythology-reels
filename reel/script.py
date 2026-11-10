"""The script: one line per scene.
hi  = Devanagari, what the voice reads (Kokoro's Hindi voice needs Devanagari)
en  = Roman Hinglish, what the captions show (same words, same order)
key = the word on which the scene's main action lands
"""
LINES = [
    dict(hi="एक छोटी सी बूटी ढूँढने गए हनुमान... और पूरा पहाड़ उठा लाए!",
         en="Ek chhoti si booti dhoondhne gaye Hanuman... aur poora pahaad utha laaye!",
         key="pahaad", title="SANJEEVNI"),
    dict(hi="युद्ध में लक्ष्मण को मेघनाद का बाण लगा, और वो बेहोश हो गए।",
         en="Yuddh mein Lakshman ko Meghnad ka baan laga, aur woh behosh ho gaye.",
         key="baan", title="LANKA"),
    dict(hi="वैद्य सुषेण बोले: सूरज उगने से पहले संजीवनी बूटी चाहिए!",
         en="Vaidya Sushen bole: Suraj ugne se pehle Sanjeevni booti chahiye!",
         key="Sanjeevni", title="SURAJ SE PEHLE"),
    dict(hi="हनुमान एक छलांग में हिमालय पहुँच गए।",
         en="Hanuman ek chhalaang mein Himalaya pahunch gaye.",
         key="chhalaang", title="HIMALAYA"),
    dict(hi="पर वहाँ हज़ारों बूटियाँ चमक रही थीं। कौन सी संजीवनी?",
         en="Par wahan hazaaron bootiyan chamak rahi thi. Kaun si Sanjeevni?",
         key="hazaaron", title="KAUN SI?"),
    dict(hi="हनुमान मुस्कुराए... और पूरा पर्वत ही उठा लिया!",
         en="Hanuman muskuraaye... aur poora parvat hi utha liya!",
         key="utha", title="POORA PARVAT"),
    dict(hi="सूरज से पहले वो लौट आए, और लक्ष्मण की आँखें खुल गईं।",
         en="Suraj se pehle woh laut aaye, aur Lakshman ki aankhein khul gayi.",
         key="khul", title="SUBAH"),
    dict(hi="इरादा पक्का हो, तो पहाड़ भी हल्का लगता है। जय बजरंगबली!",
         en="Irada pakka ho, toh pahaad bhi halka lagta hai. Jai Bajrangbali!",
         key="Bajrangbali!", title="JAI BAJRANGBALI"),
]
