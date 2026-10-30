import json, html, sys, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outfits-autumn-winter-2026.html")
e = html.escape

CATS = ["Outerwear", "Knitwear & tops", "Trousers", "Shoes", "Accessories"]
ROLE_INFO = {
    "vest_puffer": ("Outerwear", "Puffer vest"),
    "jacket_varsity": ("Outerwear", "Varsity jacket"),
    "cap_ald_yankees": ("Accessories", "Navy Yankees cap (ALD × New Era)"),
    "knit_cable_cream": ("Knitwear & tops", "Cream cable knit"),
    "knit_polo": ("Knitwear & tops", "Knit polo"),
    "knit_halfzip": ("Knitwear & tops", "Half-zip knit"),
    "shirt_oxford": ("Knitwear & tops", "Oxford shirt"),
    "shirt_overshirt": ("Knitwear & tops", "Overshirt"),
    "hoodie_graphic_blue": ("Knitwear & tops", "Blue hoodie"),
    "sweat_grey": ("Knitwear & tops", "Grey sweatshirt"),
    "tank_cream": ("Knitwear & tops", "Cream ribbed tank"),
    "tank_navy": ("Knitwear & tops", "Navy ribbed tank"),
    "tank_brown": ("Knitwear & tops", "Brown ribbed tank"),
    "clog_suede": ("Shoes", "Suede clogs"),
    "shoe_premiata": ("Shoes", "Navy suede Premiata"),
    "shoe_premiata_cream": ("Shoes", "Cream & burgundy Premiata"),
    "shoe_premiata_black": ("Shoes", "Cream & black Premiata"),
    "shoe_gg_navy": ("Shoes", "Cream & navy Golden Goose"),
    "shoe_gg_black": ("Shoes", "White & black Golden Goose"),
    "bracelet_cuff": ("Accessories", "Silver cuff"),
    "coat_wool": ("Outerwear", "Chocolate wool coat"),
    "shoe_mexico66": ("Shoes", "Cream & brown Onitsuka Mexico 66"),
    "knit_check": ("Knitwear & tops", "Cream checkerboard knit"),
    "shirt_terry": ("Knitwear & tops", "Navy terry shirt"),
    "jewelry_ring": ("Accessories", "Silver ring"),
    "jacket_suede_bomber": ("Outerwear", "Dark brown suede bomber"),
    "jacket_wool_blouson": ("Outerwear", "Dark brown wool blouson"),
    "shoe_premiata_allblack": ("Shoes", "Black Premiata Bonnie"),
    "knit_black_textured": ("Knitwear & tops", "Black textured knit"),
    "jacket_leather_brown": ("Outerwear", "Chocolate nappa leather jacket"),
    "knit_cashmere_brown": ("Knitwear & tops", "Brown cashmere crew"),
    "trouser_wool_brown": ("Trousers", "Dark brown wool wide-leg trousers"),
    "shoe_premiata_browntonal": ("Shoes", "Dark brown tonal Premiata"),
    "jacket_houndstooth": ("Outerwear", "Houndstooth Harrington"),
    "jacket_cord_burgundy": ("Outerwear", "Burgundy cord jacket"),
    "shoe_tokuten_pink": ("Shoes", "Black & pink Onitsuka Tokuten"),
    "shoe_daze_runner": ("Shoes", "Axel Arigato Daze runner"),
    "shoe_diadora_cord": ("Shoes", "Navy corduroy Diadora Equipe"),
}
ALIAS = {}
BLOCK_BRANDS_SHOES = ("Filling Pieces",)
NO_CAPS = False
SHOW_SUNGLASSES = False   # bought (Kaleos Jaconelli); the lookbook code stays for future searches
SHOW_NECKLACES = False    # bought (IX figaro, Serge DeNimes pendant)
OWNED = {
    "own_brown_puffer": ("Outerwear", "Your brown Ultra puffer"),
    "own_aircloud_brown": ("Outerwear", "Your brown AirCloud puffer"),
    "own_check_jacket": ("Outerwear", "Your check cropped jacket"),
    "own_black_puffer": ("Outerwear", "Your black puffer"),
    "own_polo_harrington": ("Outerwear", "Your Polo navy harrington"),
    "own_sage_jacket": ("Outerwear", "Your sage textured zip jacket"),
    "own_cream_cord_jacket": ("Outerwear", "Your cream cord jacket"),
    "own_brown_jacket_af": ("Outerwear", "Your brown barn jacket"),
    "own_cos_waxed": ("Outerwear", "Your COS waxed jacket"),
    "own_md_leather": ("Outerwear", "Your black Massimo Dutti nappa blouson"),
    "own_adidas_track_tan": ("Outerwear", "Your adidas Firebird twill track jacket"),
    "own_stripe_knit": ("Knitwear & tops", "Your green & cream striped knit"),
    "own_blue_linen": ("Knitwear & tops", "Your light-blue linen shirt"),
    "own_navy_linen": ("Knitwear & tops", "Your navy linen shirt"),
    "own_guinness": ("Knitwear & tops", "Your Guinness knit"),
    "own_rugby": ("Knitwear & tops", "Your Cowboys rugby polo"),
    "own_stripe_ls": ("Knitwear & tops", "Your blue striped long-sleeve"),
    "own_brown_tee": ("Knitwear & tops", "Your brown tee"),
    "own_cos_blue": ("Knitwear & tops", "Your COS slate-blue boiled merino"),
    "own_arket_blue_heavy": ("Knitwear & tops", "Your Arket blue heavy-knit jumper"),
    "own_arket_alpaca_brown": ("Knitwear & tops", "Your Arket brown alpaca-merino jumper"),
    "own_cos_cream": ("Knitwear & tops", "Your COS cream ladder-stitch jumper"),
    "own_coastal": ("Knitwear & tops", "Your Coastal crew sweater"),
    "own_blue_cable": ("Knitwear & tops", "Your blue cable knit"),
    "own_stripe_navy_green": ("Knitwear & tops", "Your navy & green striped knit"),
    "own_navy_zip_knit": ("Knitwear & tops", "Your navy striped zip knit"),
    "own_eagles": ("Knitwear & tops", "Your Eagles crew sweater"),
    "own_oasis": ("Knitwear & tops", "Your Oasis sweatshirt"),
    "own_rust_hoodie": ("Knitwear & tops", "Your rust hoodie"),
    "own_lace_camp": ("Knitwear & tops", "Your lace camp-collar shirt"),
    "own_seersucker_camp": ("Knitwear & tops", "Your adidas seersucker shirt"),
    "own_ms_brown_linen": ("Knitwear & tops", "Your brown linen shirt"),
    "own_ms_blue_stripe": ("Knitwear & tops", "Your blue striped linen shirt"),
    "own_ms_sage_stripe": ("Knitwear & tops", "Your sage striped linen shirt"),
    "own_af_white_tee": ("Knitwear & tops", "Your white A&F heavyweight tee"),
    "own_af_tee_grey": ("Knitwear & tops", "Your grey A&F heavyweight tee"),
    "own_af_tee_cream": ("Knitwear & tops", "Your cream A&F heavyweight tee"),
    "own_af_tee_black": ("Knitwear & tops", "Your black A&F heavyweight tee"),
    "own_camp_black": ("Knitwear & tops", "Your black camp-collar linen shirt"),
    "own_johnny_stripe": ("Knitwear & tops", "Your striped Johnny-collar knit polo"),
    "own_johnny_black": ("Knitwear & tops", "Your black Johnny-collar knit polo"),
    "own_af_embroidered": ("Knitwear & tops", "Your A&F embroidered linen shirt"),
    "own_af_tank_white": ("Knitwear & tops", "Your white A&F ribbed tank"),
    "own_polo_halfzip": ("Knitwear & tops", "Your Polo Ralph Lauren navy half-zip"),
    "own_crochet_diamond": ("Knitwear & tops", "Your cream & sage crochet polo"),
    "own_crochet_granny": ("Knitwear & tops", "Your granny-square crochet polo"),
    "own_ymc_grey": ("Knitwear & tops", "Your YMC grey Suedehead knit"),
    "own_arket_navy": ("Knitwear & tops", "Your Arket navy brushed-wool jumper"),
    "own_howlin_brown": ("Knitwear & tops", "Your Howlin' brown Shetland knit"),
    "own_hotel_tee": ("Knitwear & tops", "Your Nude Project Hotel tee"),
    "own_af_cream": ("Trousers", "Your cream baggy jeans"),
    "own_lightwash": ("Trousers", "Your light-wash baggy jeans"),
    "own_midwash": ("Trousers", "Your mid-blue baggy jeans"),
    "own_beige_jeans": ("Trousers", "Your khaki baggy jeans"),
    "own_af_brown": ("Trousers", "Your dark brown pleated trousers"),
    "own_af_greywash": ("Trousers", "Your grey-blue baggy jeans"),
    "own_af_linen_pullon": ("Trousers", "Your sand linen pull-on trousers"),
    "own_af_linen_baggy": ("Trousers", "Your light beige linen baggy trousers"),
    "own_levis_grey": ("Trousers", "Your Levi's 578 Baggy in neutral grey"),
    "own_levis_taupe": ("Trousers", "Your Levi's 578 Baggy cord in smokey taupe"),
    "own_af_olive_pleated": ("Trousers", "Your olive pleated baggy trousers"),
    "own_af_black_jeans": ("Trousers", "Your black baggy jeans"),
    "own_white_linen": ("Trousers", "Your white linen trousers"),
    "own_pinstripe": ("Trousers", "Your pinstripe linen trousers"),
    "own_af_black_pleated": ("Trousers", "Your black pleated baggy trousers"),
    "own_af_ash_pleated": ("Trousers", "Your ash pleated baggy trousers"),
    "own_cos_navy_trouser": ("Trousers", "Your COS navy pleated wide-leg trousers"),
    "own_becay_stripe": ("Trousers", "Your Becay cream pinstripe linen trousers"),
    "own_sn_paolo": ("Trousers", "Your Studio Nicholson Paolo cream cords"),
    "own_samba_green": ("Shoes", "Your green Handball Spezials"),
    "own_samba_maroon": ("Shoes", "Your burgundy Sambas"),
    "own_gazelle": ("Shoes", "Your light-blue Handball Spezials"),
    "own_white_sneakers": ("Shoes", "Your white Premiatas"),
    "own_premiata": ("Shoes", "Your brown Premiata Bonnies"),
    "own_spezial_cream": ("Shoes", "Your off-white Handball Spezials"),
    "own_spezial_navy": ("Shoes", "Your navy Sporty & Rich Spezials"),
    "own_watch": ("Accessories", "Your Rolex Datejust"),
    "own_cap_navy": ("Accessories", "Your navy Yankees cap"),
    "own_cap_western": ("Accessories", "Your A&F Western snapback"),
    "own_sunnies_asos": ("Accessories", "Your clear lilac round sunglasses"),
    "own_sunnies_jaconelli": ("Accessories", "Your Kaleos Jaconelli sunglasses"),
    "own_sd_pendant": ("Accessories", "Your Serge DeNimes square pendant"),
    "own_ix_figaro": ("Accessories", "Your IX figaro chain"),
    "own_ix_figaro_bracelet": ("Accessories", "Your IX figaro bracelet"),
    "own_cuban_bracelet": ("Accessories", "Your All Blues Cuban bracelet"),
    "own_ld_belt": ("Accessories", "Your Les Deux braided brown belt"),
    "own_ld_scarf": ("Accessories", "Your Les Deux navy check scarf"),
}

OUTFITS = [
  # season, name, inspo, note, pieces
  ("Autumn", "Knit & jeans", "Your board: cream knit, light jeans, burgundy Sambas, cap",
   "Your core formula, now made entirely from clothes you own: cream knit, mid-blue jeans, burgundy Sambas, navy cap.",
   ["own_cos_cream", "own_midwash", "own_samba_maroon", "cap_ald_yankees", "own_watch"]),
  ("Autumn", "Brown jacket", "Your board: brown jacket open over a knit",
   "Your brown barn jacket open over the Guinness knit, mid-blue jeans and burgundy Sambas. Dark jacket, light knit, mid denim, burgundy shoes: clear steps from dark to light, so the oatmeal knit and its graphic are the one bright thing. Barn jacket and mid-wash is the classic workwear pairing.",
   ["own_brown_jacket_af", "own_guinness", "own_midwash", "own_samba_maroon", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Autumn", "Knit polo", "Your board: brown knit polo flat lay",
   "Knit polo with light denim and your brown suede Premiatas. Smart without trying.",
   ["knit_polo", "own_lightwash", "own_premiata", "bracelet_cuff", "own_watch"]),
  ("Autumn", "Night out", "Your example: grey knit + ecru corduroy",
   "Classy with a touch of old money, but modern: your grey knit with your cream Paolo cords. Your brown suede Premiatas give the same feel as the shoes in your photo, but more relaxed. Tuck the knit loosely so your braided belt shows.",
   ["own_ymc_grey", "own_sn_paolo", "own_premiata", "own_ld_belt", "own_cuban_bracelet", "own_watch"]),
  ("Autumn", "Striped half-zip", "Your board: grey striped half-zip",
   "Your Polo Ralph Lauren half-zip over a white tee with mid-blue jeans. Easy everyday look.",
   ["own_polo_halfzip", "own_af_white_tee", "own_midwash", "own_white_sneakers", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Autumn", "Zip cardigan", "Your own navy zip knit (like the one on your board)",
   "Your navy striped zip knit over your grey tee, dark grey baggy jeans and suede clogs. The grey tee ties the knit to the jeans, softer than white.",
   ["own_navy_zip_knit", "own_af_tee_grey", "own_af_greywash", "clog_suede", "own_ix_figaro", "own_sd_pendant"]),
  ("Autumn", "Cream & brown", "Your board: cream knit + dark brown trousers",
   "Your cream jumper over your new dark brown trousers, with the burgundy Sambas as the colour pop.",
   ["own_cos_cream", "own_af_brown", "own_samba_maroon", "jewelry_ring", "own_watch"]),
  ("Autumn", "Studio day", "The reel: cream knit + stone trousers",
   "All neutrals, with suede sneakers for contrast.",
   ["own_cos_cream", "own_af_ash_pleated", "own_gazelle", "own_sd_pendant", "bracelet_cuff"]),
  ("Autumn", "Overshirt layers", "Shirts are part of your mix too",
   "Corduroy overshirt worn open over your cream tee, khaki jeans and your green Spezials. Cream is warmer than white with the brown cord and khaki.",
   ["shirt_overshirt", "own_af_tee_cream", "own_beige_jeans", "own_samba_green", "own_ix_figaro", "own_sd_pendant"]),
  ("Autumn", "Check jacket", "Your own check jacket, one step up",
   "Your check jacket and brown tee with your cream Paolo cords instead of jeans. Same Premiatas, one step smarter.",
   ["own_check_jacket", "own_brown_tee", "own_sn_paolo", "own_premiata", "own_sd_pendant", "own_watch"]),
  ("Autumn", "Stripes & brown", "Your striped knit, one step up",
   "Your green and cream striped knit over dark brown wide trousers instead of jeans. Warmer and more grown-up.",
   ["own_stripe_knit", "own_af_brown", "own_white_sneakers", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Autumn", "Stripes & sage jacket", "Your sage jacket + blue stripes",
   "Your sage textured jacket over the blue stripes, khaki jeans and navy suede Spezials. The cobalt-and-navy stripes are already the bold part, so the shoes stay calm and repeat the navy; the soft sage and khaki frame it. Want more punch? The green Spezials work too, but then two loud pieces compete.",
   ["own_sage_jacket", "own_stripe_ls", "own_beige_jeans", "own_spezial_navy", "own_cuban_bracelet", "own_sunnies_jaconelli"]),
  ("Autumn", "Guinness, upgraded", "Your Guinness knit, one step up",
   "Keep the fun knit, with navy wide trousers and your burgundy Sambas so it looks deliberate.",
   ["own_guinness", "own_cos_navy_trouser", "own_samba_maroon", "own_cuban_bracelet"]),

  ("Winter", "Brown puffer", "Your brown puffer + striped knit",
   "Your brown Ultra puffer over the navy and green striped knit, cream jeans and white sneakers.",
   ["own_brown_puffer", "own_stripe_navy_green", "own_af_cream", "own_spezial_cream", "own_watch", "cap_ald_yankees"]),
  ("Winter", "Puffer vest", "Your board: puffer vests over knits",
   "Vest over your blue cable knit with light jeans and your navy Spezials. Warm without bulk, very Copenhagen.",
   ["vest_puffer", "own_blue_cable", "own_lightwash", "own_spezial_navy", "cap_ald_yankees", "own_watch"]),
  ("Winter", "Varsity", "Your board: navy varsity + white jeans + NY cap",
   "The whisky-brown varsity over your cream tee, cream jeans and off-white Spezials, with the navy cap. Everything under the jacket is a warm cream, so it matches the brown; a bright white tee would look cold against the ivory jeans.",
   ["jacket_varsity", "own_af_tee_cream", "own_af_cream", "own_spezial_cream", "cap_ald_yankees", "own_ix_figaro"]),
  ("Winter", "Date night", "Your board: dark half-zip + wide trousers",
   "Your Polo Ralph Lauren navy half-zip, tucked loosely into your dark brown pleated trousers, with brown suede Premiatas and your Serge DeNimes pendant at the open zip. Navy and brown is the classic old-money pairing, and it stays rich in low evening light.",
   ["own_polo_halfzip", "own_af_brown", "own_premiata", "own_sd_pendant", "own_watch"]),
  ("Winter", "Grey on black", "Your board: grey knit + black wide trousers",
   "Grey knit with a white tee showing at the hem, over black wide trousers.",
   ["own_ymc_grey", "own_af_white_tee", "own_af_black_pleated", "own_spezial_cream", "jewelry_ring", "own_watch"]),
  ("Winter", "Collar & crew", "Preppy layering: shirt under a knit",
   "Oxford collar showing above a navy crewneck, ash pleated trousers and brown suede Premiatas. White, navy, stone and brown: preppy but not stiff.",
   ["shirt_oxford", "own_arket_navy", "own_af_ash_pleated", "own_premiata", "jewelry_ring", "own_watch"]),
  ("Winter", "Sweatshirt & white denim", "Your board: sweatshirt + white jeans",
   "Heavy grey sweatshirt, white jeans, your navy Spezials and the navy cap. Grey, cream and navy: simple and clean.",
   ["sweat_grey", "own_af_cream", "own_spezial_navy", "cap_ald_yankees", "own_watch"]),
  ("Winter", "Black puffer, done right", "Your black puffer, with better colours",
   "Black looks harsh with beige. Your black jeans repeat the puffer, so it belongs to the outfit, the grey knit softens it, and the off-white Spezials lift it at your feet.",
   ["own_black_puffer", "own_ymc_grey", "own_af_black_jeans", "own_spezial_cream", "own_sd_pendant", "own_watch"]),
  ("Winter", "Rainy day", "Built for Portuguese winters",
   "Your COS waxed jacket over a chocolate knit with your neutral grey Levi's. A true grey with no blue cast sits cleanly with the browns and khaki. Burgundy leather Sambas and the Western cap handle the rain better than suede, and the burgundy warms up the browns.",
   ["own_cos_waxed", "own_arket_alpaca_brown", "own_levis_grey", "own_cuban_bracelet", "own_cap_western", "own_samba_maroon"]),
  ("Winter", "Cold street", "Your board: hoodies + puffers",
   "Brown puffer over a blue hoodie with khaki jeans and your navy Spezials, which pick up the blue of the hoodie.",
   ["own_brown_puffer", "hoodie_graphic_blue", "own_beige_jeans", "own_spezial_navy", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Winter", "Coffee run", "Your photo: blue knit + check scarf",
   "Let the white tee show at the hem. Your navy, white and light-blue check scarf is the statement, and it picks up the blue knit and light jeans. The off-white Spezials add the warm contrast at your feet.",
   ["own_arket_blue_heavy", "own_af_white_tee", "own_lightwash", "own_ld_scarf", "own_sunnies_jaconelli", "own_spezial_cream"]),

  ("Summer", "Club tee", "Your board: graphic tees + clogs + cap",
   "Boxy graphic tee, white jeans, suede clogs and a cap. Easy warm-day look.",
   ["own_hotel_tee", "own_af_cream", "clog_suede", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Spring", "Knit polo & white jeans", "Your board: polo + white jeans",
   "Knit polo with white jeans and your navy suede Spezials. Brown, cream and navy: the classiest spring look here.",
   ["knit_polo", "own_af_cream", "own_spezial_navy", "own_sunnies_jaconelli", "bracelet_cuff"]),
  ("Spring", "Blue knit & graphic", "Your board: blue knit + graphic tee flat lay",
   "Blue knit over a graphic tee, light jeans and your white Premiatas.",
   ["own_arket_blue_heavy", "own_hotel_tee", "own_lightwash", "own_white_sneakers", "own_sd_pendant", "own_cuban_bracelet"]),
  ("Spring", "Weekend hoodie", "Your rust hoodie",
   "Rust hoodie, dark grey baggy jeans, white Premiatas and the navy cap. All yours.",
   ["own_rust_hoodie", "own_af_greywash", "own_white_sneakers", "cap_ald_yankees", "own_watch"]),
  ("Spring", "Oxford & stone", "Shirts for the first warm days",
   "Oxford shirt with sleeves rolled, stone pleated trousers, your white Premiatas.",
   ["shirt_oxford", "own_af_ash_pleated", "own_white_sneakers", "own_sunnies_jaconelli", "own_ld_belt", "bracelet_cuff"]),
  ("Spring", "Linen layers", "Your light-blue linen shirt, for spring",
   "Light-blue linen shirt with the top two buttons open over your white ribbed tank, stone trousers and your light-blue Spezials. Blue suits you.",
   ["own_blue_linen", "own_af_tank_white", "own_af_ash_pleated", "own_gazelle", "own_sunnies_asos", "own_cuban_bracelet"]),
  ("Summer", "Navy & white", "Your navy linen shirt and white trousers",
   "The outfit you already wear, finished with clogs, the Rolex and the Cuban bracelet.",
   ["own_navy_linen", "own_white_linen", "clog_suede", "own_cuban_bracelet", "own_watch"]),
  ("Summer", "Pinstripe & graphic", "Your pinstripe trousers + your board (graphic tee, clogs)",
   "Your pinstripe linen trousers with a boxy graphic tee and clogs. Relaxed, a bit resort.",
   ["own_hotel_tee", "own_pinstripe", "clog_suede", "cap_ald_yankees", "own_ix_figaro", "own_sd_pendant"]),
  ("Spring", "Rugby & navy", "Your Cowboys rugby polo, one step up",
   "Your Cowboys rugby polo with navy wide trousers. More contrast than the all-white version.",
   ["own_rugby", "own_cos_navy_trouser", "own_white_sneakers", "own_sunnies_jaconelli", "own_cuban_bracelet"]),
  ("Spring", "Sunday lunch", "Built from your style",
   "Chocolate knit, navy wide trousers and your light-blue Spezials. Brown, navy and light blue is a classic mix, and the pale blue at your feet is the contrast that lifts two dark colours.",
   ["own_arket_alpaca_brown", "own_cos_navy_trouser", "own_gazelle", "own_ix_figaro", "own_watch"]),
  ("Autumn", "Blue & brown", "Your new COS jumper + your new brown trousers",
   "Light blue and dark brown is one of the best combinations for your colouring. Brown suede Premiatas tie it together.",
   ["own_arket_blue_heavy", "own_af_brown", "own_premiata", "own_cuban_bracelet", "own_watch"]),
  ("Autumn", "Check & navy", "Your check jacket, with navy",
   "Check jacket open over a navy knit, cream jeans and burgundy Sambas. The navy picks up the check.",
   ["own_check_jacket", "own_arket_navy", "own_af_cream", "own_samba_maroon", "own_watch", "own_sd_pendant"]),
  ("Autumn", "Brown & burgundy", "Your board formula, in brown",
   "Chocolate knit, light jeans, burgundy Sambas, your cream and brown Western cap and your Serge DeNimes pendant over the knit. Warm and easy.",
   ["own_arket_alpaca_brown", "own_lightwash", "own_samba_maroon", "own_cap_western", "own_sd_pendant"]),
  ("Winter", "Tonal brown", "Your brown puffer, head to toe",
   "Your brown AirCloud puffer, cream jumper, dark brown trousers and brown suede Premiatas. Warm, tonal and classy.",
   ["own_aircloud_brown", "own_cos_cream", "own_af_brown", "own_premiata", "own_watch", "own_sd_pendant"]),
  ("Winter", "Black puffer & burgundy", "Your black puffer with a colour pop",
   "Black puffer over your light-grey Oasis sweatshirt with mid-blue jeans. Black and light grey is a clean contrast, and the burgundy Sambas are the colour pop. No navy next to the black.",
   ["own_black_puffer", "own_oasis", "own_midwash", "own_samba_maroon", "own_watch", "own_cuban_bracelet"]),
  ("Spring", "Blue & cream", "Your Arket blue jumper, spring version",
   "Light blue jumper with cream jeans and your navy Sporty & Rich Spezials. Exactly the Sporty & Rich look, and all the clothes are yours.",
   ["own_arket_blue_heavy", "own_af_cream", "own_spezial_navy", "own_sunnies_asos", "own_watch"]),
  ("Spring", "Cowboys & khaki", "Your rugby polo with khaki jeans",
   "Your Cowboys rugby polo with khaki jeans, navy Spezials and the navy cap. Collegiate preppy, the same idea as the Sporty & Rich collab.",
   ["own_rugby", "own_beige_jeans", "own_spezial_navy", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Summer", "Riviera tee", "Summer, softer and more casual",
   "Your white tee with white linen trousers, light-blue Spezials, your clear lilac sunglasses and the IX figaro chain and bracelet. Crisp white on white keeps every colour cool and pastel; a buttery cream tee would look yellow next to the bright white linen.",
   ["own_af_white_tee", "own_white_linen", "own_gazelle", "own_sunnies_asos", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Summer", "Camp collar", "Your lace camp-collar shirt",
   "Your lace camp-collar shirt worn open, cream jeans and suede clogs.",
   ["own_lace_camp", "own_af_cream", "clog_suede", "own_sunnies_jaconelli", "own_ix_figaro", "own_sd_pendant"]),
  ("Summer", "Blue linen & olive", "Your light-blue linen shirt",
   "Your light-blue linen shirt, top two buttons open over your white tank, your olive pleated baggy trousers, white Premiatas and the navy cap. Blue and olive is a fresh summer pairing.",
   ["own_blue_linen", "own_af_tank_white", "own_af_olive_pleated", "own_white_sneakers", "cap_ald_yankees", "own_ix_figaro"]),
  ("Summer", "Graphic & light denim", "Your board: graphic tees",
   "Your Hotel tee with light-wash baggy jeans, navy Spezials and the cap, plus the layered necklaces. Summer street, no shorts.",
   ["own_hotel_tee", "own_lightwash", "own_spezial_navy", "cap_ald_yankees", "own_ix_figaro", "own_sd_pendant"]),
  ("Summer", "Summer dinner", "Brown linen at night",
   "Your brown linen shirt, stone pleated trousers, brown suede Premiatas and the Rolex. Classy for warm evenings.",
   ["own_ms_brown_linen", "own_af_ash_pleated", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Summer", "Summer night tee", "A tee, dressed up for a warm night",
   "Your grey tee with ash pleated trousers, brown suede Premiatas, the layered necklaces and the Rolex. Easy but put together.",
   ["own_af_tee_grey", "own_af_ash_pleated", "own_premiata", "own_ix_figaro", "own_sd_pendant", "own_watch"]),
  ("Summer", "Beach town", "Your navy linen shirt",
   "Navy linen shirt, top two buttons open over your white tank, your light beige linen baggy trousers, suede clogs and your havana Jaconellis. Long and light instead of shorts.",
   ["own_navy_linen", "own_af_tank_white", "own_af_linen_baggy", "clog_suede", "own_sunnies_jaconelli", "own_ix_figaro"]),
  ("Summer", "Khaki & blue", "Your khaki jeans + blue linen",
   "Light-blue linen shirt, khaki jeans and white Premiatas. Easy for a city day.",
   ["own_blue_linen", "own_beige_jeans", "own_white_sneakers", "own_sunnies_jaconelli", "bracelet_cuff"]),
  ("Summer", "Day in Porto", "Tee, casual",
   "Your cream tee with khaki jeans, burgundy Sambas and your Western cap, whose brown brim picks up the khaki.",
   ["own_af_tee_cream", "own_beige_jeans", "own_samba_maroon", "own_cap_western", "own_sunnies_jaconelli"]),
  ("Autumn", "Navy harrington", "Your Polo harrington, old-money style",
   "Your navy Polo harrington over the Coastal sweater, khaki jeans and brown suede Premiatas. Pure old money, and all yours.",
   ["own_polo_harrington", "own_coastal", "own_beige_jeans", "own_premiata", "own_watch", "own_sunnies_jaconelli"]),
  ("Autumn", "Cream cord & Eagles", "Your cord jacket + Eagles sweater",
   "Cream cord jacket open over the Eagles sweater, light jeans, green Spezials and your cream Western cap. Preppy sport.",
   ["own_cream_cord_jacket", "own_eagles", "own_lightwash", "own_samba_green", "own_cap_western", "own_cuban_bracelet"]),
  ("Autumn", "Coastal & navy", "Your Coastal sweater",
   "Coastal sweater with navy wide trousers, burgundy Sambas and the cap.",
   ["own_coastal", "own_cos_navy_trouser", "own_samba_maroon", "cap_ald_yankees", "own_watch"]),
  ("Autumn", "Oasis day", "Your Oasis sweatshirt, as you wore it",
   "Oasis sweatshirt with your dark grey baggy jeans, burgundy Sambas and the cap. Street, but considered.",
   ["own_oasis", "own_af_greywash", "own_samba_maroon", "cap_ald_yankees", "own_sd_pendant"]),
  ("Autumn", "Blue cable & grey", "Your blue cable knit",
   "Your dusty-blue cable knit, dark grey jeans, off-white Spezials and the navy cap. The clothes stay in one cool grey-blue palette, and the cream-and-burgundy Spezials are the contrast at your feet.",
   ["own_blue_cable", "own_af_greywash", "own_spezial_cream", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Winter", "Cord jacket & stripes", "Your cream cord jacket, winter",
   "Cream cord jacket over the navy and green striped knit, mid-blue jeans and brown Premiatas.",
   ["own_cream_cord_jacket", "own_stripe_navy_green", "own_midwash", "own_premiata", "own_watch", "cap_ald_yankees"]),
  ("Spring", "Harrington & white", "Your Polo harrington, lighter",
   "Navy harrington over a white tee with cream jeans and white sneakers. Clean and classic.",
   ["own_polo_harrington", "own_af_white_tee", "own_af_cream", "own_spezial_cream", "own_sunnies_jaconelli", "own_watch"]),
  ("Spring", "Sage & brown", "Your sage jacket + brown trousers",
   "Sage textured jacket over your cream tee, dark brown trousers and white Premiatas. Cream sits more softly between sage and brown than white.",
   ["own_sage_jacket", "own_af_tee_cream", "own_af_brown", "own_white_sneakers", "own_sd_pendant", "own_sunnies_jaconelli"]),
  ("Spring", "Navy zip & khaki", "Your navy zip knit, smarter",
   "Navy zip knit half-open over your light-blue linen shirt, collar out, with khaki jeans, brown suede Premiatas and the Rolex. Navy, light blue and khaki: classic.",
   ["own_navy_zip_knit", "own_blue_linen", "own_beige_jeans", "own_premiata", "own_watch"]),
  ("Summer", "Seersucker & denim", "Your adidas seersucker shirt",
   "Your adidas seersucker shirt worn open over nothing, with mid-blue baggy jeans, brown suede Premiatas, the IX chain and the Rolex. The shirt is sporty, so it reads best as relaxed daytime: the warm off-white against mid-blue denim is the classic summer contrast, and the brown suede grounds it. Mid-blue rather than light-wash, because the icy wash looks cold next to the shirt's warm white.",
   ["own_seersucker_camp", "own_midwash", "own_premiata", "own_watch", "own_ix_figaro"]),
  ("Summer", "Sage stripes", "Your sage striped linen shirt",
   "Sage striped linen shirt, top two buttons open over your white tank, ash pleated trousers, white Premiatas and your clear lilac sunglasses. Soft pastels together.",
   ["own_ms_sage_stripe", "own_af_tank_white", "own_af_ash_pleated", "own_white_sneakers", "own_sunnies_asos", "own_cuban_bracelet"]),
  ("Summer", "Blue stripes & denim", "Your blue striped linen shirt",
   "Blue striped linen shirt, top two buttons open over your white tank, light-wash baggy jeans, burgundy Sambas and the cap.",
   ["own_ms_blue_stripe", "own_af_tank_white", "own_lightwash", "own_samba_maroon", "cap_ald_yankees", "own_sd_pendant"]),
  ("Summer", "Brown linen day", "Your brown linen shirt, open",
   "Brown linen shirt, top two buttons open over your white tank, cream jeans and light-blue Spezials. A cream tank is even softer with the brown.",
   ["own_ms_brown_linen", "own_af_tank_white", "own_af_cream", "own_gazelle", "own_sunnies_jaconelli", "own_cuban_bracelet"]),
  ("Winter", "AirCloud & cable", "Your second brown puffer",
   "Brown AirCloud puffer over your blue cable knit, cream jeans, burgundy Sambas and your cream and brown Western cap. All yours.",
   ["own_aircloud_brown", "own_blue_cable", "own_af_cream", "own_samba_maroon", "own_cap_western", "own_watch"]),
  ("Autumn", "Cream & black", "Your black jeans, done right",
   "Cream cord jacket open over your white tee, black baggy jeans and the green Spezials. Light colours on top keep the black from looking heavy on you. All yours.",
   ["own_cream_cord_jacket", "own_af_white_tee", "own_af_black_jeans", "own_samba_green", "own_cuban_bracelet", "own_sd_pendant"]),
  ("Winter", "Blue on black", "Your black pleated trousers, done right",
   "Light-blue cable knit over your black pleated trousers with white Premiatas, the Cuban bracelet and the Rolex. Light top, black trousers, white shoes: crisp, with no brown to fight the black.",
   ["own_blue_cable", "own_af_black_pleated", "own_white_sneakers", "own_cuban_bracelet", "own_watch"]),
  ("Summer", "White tee & olive", "Tee and light trousers",
   "Your white tee with your olive pleated baggy trousers, navy Spezials, the navy cap and the IX figaro chain and bracelet. Casual, and navy with olive works.",
   ["own_af_white_tee", "own_af_olive_pleated", "own_spezial_navy", "cap_ald_yankees", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Summer", "Brown tee & cream", "Warm summer neutrals",
   "Your brown tee with cream jeans, light-blue Spezials, your Western cap and the Cuban bracelet. Warm, with one cool accent at the feet.",
   ["own_brown_tee", "own_af_cream", "own_gazelle", "own_cap_western", "own_cuban_bracelet"]),
  ("Summer", "Grey tee & navy", "Summer evening, casual",
   "Your grey tee with the COS navy wide-leg trousers, white Premiatas and the layered necklaces. Simple and cool-toned for a warm evening.",
   ["own_af_tee_grey", "own_cos_navy_trouser", "own_white_sneakers", "own_ix_figaro", "own_sd_pendant"]),
  ("Summer", "Hotel tee & khaki", "Your board: graphic tees",
   "Your Hotel tee with khaki jeans, green Spezials and the navy cap. Ivory, khaki and a green accent.",
   ["own_hotel_tee", "own_beige_jeans", "own_samba_green", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Summer", "Cream tee & light denim", "The easiest summer outfit",
   "Your cream tee with light-wash baggy jeans, white Premiatas, the navy cap and your clear lilac sunglasses.",
   ["own_af_tee_cream", "own_lightwash", "own_white_sneakers", "cap_ald_yankees", "own_sunnies_asos"]),
  ("Summer", "Granny squares", "Your crochet polo, street",
   "Your granny-square crochet polo, unbuttoned a little lower over your white tank, with cream jeans, burgundy Sambas, your Western cap and the Cuban bracelet. The red-brown squares pick up the Sambas and the cap's brown brim.",
   ["own_crochet_granny", "own_af_tank_white", "own_af_cream", "own_samba_maroon", "own_cap_western", "own_cuban_bracelet"]),
  ("Summer", "Sage crochet", "Your crochet polo, soft and light",
   "Your cream and sage crochet polo, unbuttoned a little lower over your white tank, with ash pleated trousers, white Premiatas, your clear lilac sunglasses and the IX chain and bracelet. Soft pastels, no shorts.",
   ["own_crochet_diamond", "own_af_tank_white", "own_af_ash_pleated", "own_white_sneakers", "own_sunnies_asos", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Summer", "Johnny collar & navy", "Your striped knit polo, dressed up",
   "Your striped Johnny-collar polo with the COS navy wide-leg trousers, brown suede Premiatas, the IX chain and the Rolex. Beige, navy and brown: easy old money for a summer dinner.",
   ["own_johnny_stripe", "own_cos_navy_trouser", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Summer", "Black knit & cream", "Your black Johnny-collar polo",
   "Your black Johnny-collar polo with cream jeans, off-white Spezials, the IX chain and the Rolex. Light trousers and shoes keep the black from feeling heavy, and the silver chain pops on black.",
   ["own_johnny_black", "own_af_cream", "own_spezial_cream", "own_ix_figaro", "own_watch"]),
  ("Summer", "Black camp night", "Your black camp-collar shirt",
   "Your black camp-collar shirt worn open with nothing underneath, white linen trousers, white Premiatas and the layered necklaces on skin. The silver chains break up the black at your neck.",
   ["own_camp_black", "own_white_linen", "own_white_sneakers", "own_ix_figaro", "own_sd_pendant"]),
  ("Summer", "Sage stripes & linen", "Your mirror photo: sage stripes, white tank, linen",
   "Your sage striped linen shirt, top two buttons open over your white tank, your light beige linen baggy trousers, brown suede Premiatas and your Serge DeNimes pendant. Your mirror-photo look, with a wider, straighter trouser and shoes.",
   ["own_ms_sage_stripe", "own_af_tank_white", "own_af_linen_baggy", "own_premiata", "own_sd_pendant", "own_cuban_bracelet"]),
  ("Summer", "Sage stripes & khaki", "Your casino-night look in Espinho",
   "Your sage striped linen shirt with the top buttons open over the white tank, khaki baggy jeans and brown suede Premiatas, with the Serge DeNimes pendant and the Rolex. Earthy and easy: the darker suede anchors the sage and khaki. For summer evenings and warm early-autumn ones; bring the brown barn jacket if it cools down.",
   ["own_ms_sage_stripe", "own_af_tank_white", "own_beige_jeans", "own_premiata", "own_sd_pendant", "own_watch"]),
  ("Summer", "Navy & cream tank", "A cream tank under navy linen",
   "Navy linen shirt, top two buttons open over a cream ribbed tank, cream baggy jeans, burgundy Sambas and your Western cap. Navy, cream and burgundy: preppy and warm.",
   ["own_navy_linen", "tank_cream", "own_af_cream", "own_samba_maroon", "own_cap_western", "own_cuban_bracelet"]),
  ("Summer", "Blue & brown Riviera", "A brown tank under light-blue linen",
   "Light-blue linen shirt, top two buttons open over a chocolate ribbed tank, white linen trousers, brown suede Premiatas, the IX chain and the Rolex. Light blue and brown, your best pairing, made summery.",
   ["own_blue_linen", "tank_brown", "own_white_linen", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Summer", "Stripes & navy tank", "A navy tank under blue stripes",
   "Blue striped linen shirt, top two buttons open over a navy ribbed tank, ash pleated trousers, white Premiatas and the Rolex. Blue, navy and stone: easy old money for lunch.",
   ["own_ms_blue_stripe", "tank_navy", "own_af_ash_pleated", "own_white_sneakers", "own_watch", "own_cuban_bracelet"]),
  ("Summer", "Black polo & pinstripe", "Riviera evening: black knit polo, cream pinstripe linen",
   "Your black Johnny-collar knit polo with the Becay cream pinstripe linen trousers and the off-white Spezials, plus the IX chain and the Rolex. Black against cream is the classic summer-evening contrast, the knit polo keeps it smart, and the fine tan stripe gives the linen more interest than plain cream.",
   ["own_johnny_black", "own_becay_stripe", "own_spezial_cream", "own_ix_figaro", "own_watch"]),
  ("Summer", "Blue linen & pinstripe", "Day out: light-blue linen over a tank, cream pinstripe",
   "Your light-blue linen shirt, top two buttons open over the white tank, with the Becay cream pinstripe linen trousers and brown suede Premiatas, plus the Kaleos sunglasses and the IX chain. Light blue, cream and brown is the easiest Riviera palette, and the tan pinstripe ties the trousers to the brown suede.",
   ["own_blue_linen", "own_af_tank_white", "own_becay_stripe", "own_premiata", "own_sunnies_jaconelli", "own_ix_figaro"]),
  ("Summer", "Brown linen & pinstripe", "Warm and tonal: dark brown linen, cream pinstripe",
   "Your dark brown linen shirt, top two buttons open over the white tank, with the Becay cream pinstripe linen trousers and the light-blue Spezials, plus the Kaleos sunglasses and the IX chain. The tan stripe picks up the brown shirt, so the outfit reads as one warm piece, and the light-blue shoes are the one cool accent.",
   ["own_ms_brown_linen", "own_af_tank_white", "own_becay_stripe", "own_gazelle", "own_sunnies_jaconelli", "own_ix_figaro"]),
  ("Autumn", "Navy & taupe cord", "Your new Levi's taupe cord",
   "Your Arket navy jumper with the taupe Levi's cord, burgundy Sambas and the navy cap. Navy and taupe are softer than navy and khaki, and the burgundy gives it a lift.",
   ["own_arket_navy", "own_levis_taupe", "own_samba_maroon", "cap_ald_yankees", "own_cuban_bracelet"]),
  ("Autumn", "Brown & grey", "Your new grey Levi's",
   "Your brown barn jacket over the cream ladder-stitch knit, neutral grey Levi's and brown suede Premiatas. Brown, cream and a true grey: very Copenhagen.",
   ["own_brown_jacket_af", "own_cos_cream", "own_levis_grey", "own_premiata", "own_watch", "own_sd_pendant"]),
  ("Winter", "Taupe & light blue", "Your Levi's taupe cord, winter",
   "Dark brown puffer over your light-blue COS jumper, taupe Levi's cord, off-white Spezials and your navy check scarf. The scarf ties the light blue to the warm browns.",
   ["own_brown_puffer", "own_arket_blue_heavy", "own_levis_taupe", "own_spezial_cream", "own_ld_scarf", "own_watch"]),
  ("Winter", "Tonal grey", "Your grey Levi's, winter",
   "Brown AirCloud puffer over your grey YMC knit with the grey Levi's, burgundy Sambas and the Western cap. Grey on grey, warmed up by the brown and burgundy.",
   ["own_aircloud_brown", "own_ymc_grey", "own_levis_grey", "own_samba_maroon", "own_cap_western", "own_cuban_bracelet"]),
  ("Autumn", "Waxed & navy", "The COS waxed jacket, dressed for the city",
   "Your COS waxed jacket over the Arket navy brushed-wool jumper, ash pleated baggies and brown suede Premiatas, with the Rolex and the All Blues bracelet. Khaki with a chocolate cord collar over navy is the classic country-meets-city pairing: the ash trousers keep it light, and the brown suede picks up the collar. The dark knit also means no wax marks on light wool.",
   ["own_cos_waxed", "own_arket_navy", "own_af_ash_pleated", "own_premiata", "own_watch", "own_cuban_bracelet"]),
  ("Winter", "Waxed & cream cord", "The COS waxed jacket, winter",
   "Your COS waxed jacket over your cream ladder-stitch knit, taupe Levi's cord and burgundy Sambas. The chocolate cord collar picks up the cord trousers, and the leather Sambas cope with rain.",
   ["own_cos_waxed", "own_cos_cream", "own_levis_taupe", "own_samba_maroon", "own_watch", "own_sd_pendant"]),
  ("Autumn", "Paolo & cream tee", "Your fitting: Studio Nicholson cords + A&F tee",
   "Your cream heavyweight tee with the Studio Nicholson Paolo cords in Panna and brown suede Premiatas, with the IX chain and bracelet. Cream on panna is one warm tone, so the cord's texture does the work; bright white next to panna makes the cords look yellow. Add the brown barn jacket when it cools down.",
   ["own_af_tee_cream", "own_sn_paolo", "own_premiata", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Autumn", "Brown linen & taupe cord", "Between seasons: your brown shirt with the taupe cords",
   "Your dark brown linen shirt with the top buttons open over the white ribbed tank, the Levi's taupe cords and light-blue Spezials, with the IX chain, the All Blues bracelet and the Kaleos by day. Rich brown over smokey taupe is one earthy family at two depths, and the white tank lifts it at the neck. The clothes are quiet, so the light-blue Spezials are the contrast. Spring or autumn: add a light jacket when it cools.",
   ["own_ms_brown_linen", "own_af_tank_white", "own_levis_taupe", "own_gazelle", "own_ix_figaro", "own_cuban_bracelet", "own_sunnies_jaconelli"]),
  ("Special Summer", "Navy terry Riviera", "New piece: navy cable-terry shirt",
   "Navy cable-terry shirt with the top buttons open, your light beige linen baggy trousers, brown suede Premiatas, the IX chain and the Rolex. The Riviera in the evening.",
   ["shirt_terry", "own_af_linen_baggy", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Special Winter", "Chocolate coat", "New piece: chocolate wool coat",
   "Chocolate wool coat over your Arket navy jumper, ash pleated trousers, white Premiatas and your navy check scarf. Brown, navy and stone: the classiest winter look here, with the white Premiatas as the fresh contrast underneath.",
   ["coat_wool", "own_arket_navy", "own_af_ash_pleated", "own_white_sneakers", "own_ld_scarf", "own_watch"]),
  ("Special Summer", "Embroidered linen night", "Special piece: A&F embroidered linen shirt",
   "Your warm-beige A&F linen shirt with tonal embroidered medallions, top two buttons open, your COS navy pleated wide-leg trousers, brown suede Premiatas, the IX chain and the Rolex. A deep, neutral navy under the beige gives the contrast the olive lacked.",
   ["own_af_embroidered", "own_cos_navy_trouser", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Special Winter", "Checkerboard knit", "Special piece: Les Deux check knit",
   "Les Deux's cream checkerboard wool knit with mid-blue baggy jeans, brown suede Premiatas and your brown AirCloud puffer worn open. A modern knit that keeps your cream-and-brown palette.",
   ["own_aircloud_brown", "knit_check", "own_midwash", "own_premiata", "own_watch"]),
  ("Special Autumn", "Country dinner", "Relaxed dinner: the waxed jacket, dressed up",
   "Your COS waxed jacket over the Arket dark brown alpaca-merino, Studio Nicholson cream cords and brown Premiatas, with the Rolex and the All Blues bracelet. The jacket's chocolate cord collar picks up the brown knit and the suede, and the cream cords lift it for dinner. Leave the knit untucked. The dark knit keeps the jacket's wax off light wool.",
   ["own_cos_waxed", "own_arket_alpaca_brown", "own_sn_paolo", "own_premiata", "own_watch", "own_cuban_bracelet"]),
  ("Special Autumn", "Houndstooth & green", "Standout: Pop houndstooth Harrington",
   "Pop Trading Company's brown houndstooth Harrington over your cream tee and cream baggy jeans, with your green Spezials. The jacket's green quilted lining answers the shoes, so the two standouts talk to each other on a calm cream base.",
   ["jacket_houndstooth", "own_af_tee_cream", "own_af_cream", "own_samba_green", "own_ix_figaro", "own_watch"]),
  ("Special Autumn", "Burgundy cord", "Standout: Percival burgundy cord jacket",
   "Percival's cropped burgundy cord jacket over your grey heavyweight tee, grey Levi's and the off-white Spezials, whose burgundy stripes pick up the jacket. Grey keeps the burgundy rich, not loud.",
   ["jacket_cord_burgundy", "own_af_tee_grey", "own_levis_grey", "own_spezial_cream", "own_ix_figaro", "own_watch"]),
  ("Special Winter", "Pink stripe night", "Standout: black and pink Onitsuka Tokuten",
   "Your grey YMC knit with black pleated trousers and Onitsuka Tokuten in black suede with pink stripes. It breaks your usual light-shoe habit with black trousers on purpose: the pink stripes do the lifting.",
   ["own_ymc_grey", "own_af_black_pleated", "shoe_tokuten_pink", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Spring", "Blue runner day", "Standout: Axel Arigato Daze runners",
   "Your light-blue linen shirt with the top buttons open over the white tank, grey Levi's and Axel Arigato's slim Daze runners in blue suede and grey, with a burgundy heel tab. Blues and greys with one warm accent. Jaconellis by day.",
   ["own_blue_linen", "own_af_tank_white", "own_levis_grey", "shoe_daze_runner", "own_sunnies_jaconelli", "own_sd_pendant"]),
  ("Special Autumn", "Black leather & grey", "Standout: Massimo Dutti black nappa blouson",
   "Massimo Dutti's black nappa blouson over your YMC grey Suedehead knit, black pleated baggy trousers and burgundy Sambas, with the Rolex and the IX bracelet. The black trousers repeat the jacket, so the leather belongs to the outfit instead of sitting on top of it; the soft grey knit keeps it from looking hard, and the burgundy at your feet is the one warm note. Silver only.",
   ["own_md_leather", "own_ymc_grey", "own_af_black_pleated", "own_samba_maroon", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Autumn", "Black leather, white tee", "Built around the black nappa blouson",
   "Massimo Dutti's black nappa blouson over your white heavyweight tee, black pleated baggy trousers and black Premiata Bonnies with silver stripes, plus the IX chain and the Rolex. Black from shoulder to shoe; the white tee at the neck and hem keeps it sharp, and the silver picks up the shoes' stripes.",
   ["own_md_leather", "own_af_white_tee", "own_af_black_pleated", "shoe_premiata_allblack", "own_ix_figaro", "own_watch"]),
  ("Special Winter", "All black, textured", "Full black: leather, ribbed knit, wool-feel trousers",
   "The black nappa blouson over A&F's black ribbed cotton crew, black pleated baggy trousers and black Premiata Bonnies, with the Rolex and the IX bracelet. Full black works because every layer has a different texture: smooth leather, ribbed cotton, matte trousers and suede. The silver on the wrists and shoes does the lifting.",
   ["own_md_leather", "knit_black_textured", "own_af_black_pleated", "shoe_premiata_allblack", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Autumn", "Tonal chocolate", "Elegant, one colour: the suede bomber you picked",
   "All chocolate in four textures: the COS mahogany suede bomber, your Arket brushed alpaca-merino in dark brown, the dark brown pleated trousers and brown suede Bonnies, with the Rolex and the IX bracelet. One colour, so the textures do the work, and the silver lifts it.",
   ["jacket_suede_bomber", "own_arket_alpaca_brown", "own_af_brown", "own_premiata", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Autumn", "Chocolate leather", "Elegant: the warm twin of your black leather jacket",
   "Massimo Dutti's chocolate nappa jacket over your cream ladder-stitch knit, dark brown pleated trousers and brown suede Bonnies, with the Rolex and the IX bracelet. Cream between two browns keeps it light; the same idea as your black leather looks, warmer.",
   ["jacket_leather_brown", "own_cos_cream", "own_af_brown", "own_premiata", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Autumn", "Poker table", "Poker night: give nothing away",
   "Tonal from the top down: your adidas Firebird cotton-twill track jacket (Blanch Cargo) over the Nude Project ivory tee, the Studio Nicholson cream cords and your A&F Western snapback, with the navy suede Sporty & Rich Spezials as the one dark anchor, plus the Kaleos sunglasses if you want them and the IX chain. The boxy, cropped jacket over wide cords is your best shape, and a track top is a poker-room classic: comfortable for hours and easy to unzip or hang on the chair. Dressed the way poker players do: the cap and sunglasses hide your eyes, a layer you can take off for hours in casino air-conditioning, quiet colours that give nothing away, and no Rolex or bracelets, so nothing signals money or clinks against the chips.",
   ["own_adidas_track_tan", "own_hotel_tee", "own_sn_paolo", "own_spezial_navy", "own_cap_western", "own_sunnies_jaconelli", "own_ix_figaro"]),
  ("Special Autumn", "Embroidered shirt & black", "Day to dinner: the embroidered shirt with black",
   "Your A&F embroidered linen shirt in warm beige, top two buttons open, with the black pleated baggy trousers and white Premiatas, plus the IX chain. Warm beige against black looks dressed up without trying, and the linen keeps you cool through a warm day. Wear the Kaleos sunglasses in the daytime and swap them for the Rolex at dinner.",
   ["own_af_embroidered", "own_af_black_pleated", "own_white_sneakers", "own_ix_figaro", "own_sunnies_jaconelli", "own_watch"]),
  ("Special Autumn", "Black leather & ivory", "Standout: Massimo Dutti black nappa blouson",
   "The black nappa blouson over one column of ivory: your COS cream ladder-stitch, the A&F cream jeans and the off-white Premiatas, with the Rolex and the IX bracelet. The knit and the jeans are the same soft ivory, so the light half reads as one piece and the leather frames it. The black star on the Premiatas repeats the jacket at your feet, and silver keeps it cool.",
   ["own_md_leather", "own_cos_cream", "own_af_cream", "own_white_sneakers", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Autumn", "Black leather & ice denim", "Standout: Massimo Dutti black nappa blouson",
   "The classic: the black nappa blouson over your bright white A&F tee, the icy light-wash baggy jeans and the off-white Premiatas, with the IX chain and the Rolex. Everything under the jacket is cool (pure white, pale blue, white shoes with black details), so the black sits naturally on top.",
   ["own_md_leather", "own_af_white_tee", "own_lightwash", "own_white_sneakers", "own_ix_figaro", "own_watch"]),
  ("Special Autumn", "Black leather & panna cord", "Standout: Massimo Dutti black nappa blouson",
   "The black nappa blouson over a warm cream column: your A&F cream tee, the Studio Nicholson panna cords and the off-white Spezials, with the IX chain and the Rolex. The cream tee instead of a bright white one, because pure white next to panna makes the cords look yellow; the Spezials' off-white and gum sole stay in the same warm family.",
   ["own_md_leather", "own_af_tee_cream", "own_sn_paolo", "own_spezial_cream", "own_ix_figaro", "own_watch"]),
  ("Special Autumn", "Slate blue & navy", "Your COS boiled merino in L, dressed for dinner",
   "Your COS slate-blue boiled merino over the COS navy pleated wide-leg trousers and brown suede Premiatas, with the Rolex and the All Blues bracelet. The soft, greyed blue over deep navy is one cool column from light to dark, and the brown suede is the single warm note. Smooth boiled merino is dressier than a chunky knit, so this one works for dinner.",
   ["own_cos_blue", "own_cos_navy_trouser", "own_premiata", "own_watch", "own_cuban_bracelet"]),
  ("Special Autumn", "Black leather & slate blue", "Standout: Massimo Dutti black nappa blouson",
   "The black nappa blouson over your COS slate-blue boiled merino, the neutral grey Levi's and the off-white Premiatas, with the Rolex and the IX bracelet. Everything under the jacket is cool and slightly greyed (blue, grey, off-white with black details), so the black belongs; the Premiatas' black star repeats the jacket at your feet.",
   ["own_md_leather", "own_cos_blue", "own_levis_grey", "own_white_sneakers", "own_watch", "own_ix_figaro_bracelet"]),
  ("Special Autumn", "Black leather & grey tee", "Train by day, Seinfeld at night",
   "Your grey A&F tee, black baggy jeans and burgundy Sambas all day, then the black nappa blouson on top for the night, with the IX chain and the Rolex. The black jeans repeat the jacket, so the leather belongs; the cool grey tee keeps the black-and-grey idea of #98 but light enough for a warm day, and the burgundy Sambas are the contrast at your feet. By day, Kaleos instead of the Rolex.",
   ["own_md_leather", "own_af_tee_grey", "own_af_black_jeans", "own_samba_maroon", "own_ix_figaro", "own_watch"]),
]

# backup inner layer per outfit, for when the main one is in the wash (first is the best swap)
INNER_ALT = {
  "Striped half-zip": ["own_af_tee_grey", "own_hotel_tee"],
  "Zip cardigan": ["own_af_white_tee", "own_hotel_tee"],
  "Overshirt layers": ["own_af_white_tee", "own_hotel_tee"],
  "Check jacket": ["own_af_white_tee", "own_af_tee_cream"],
  "Stripes & sage jacket": ["own_af_white_tee", "own_af_tee_cream"],
  "Varsity": ["own_hotel_tee"],
  "Grey on black": ["own_af_tee_black", "own_hotel_tee"],
  "Collar & crew": ["own_blue_linen", "own_ms_blue_stripe"],
  "Coffee run": ["own_af_tee_grey", "own_hotel_tee"],
  "Club tee": ["own_af_white_tee", "own_af_tee_cream"],
  "Blue knit & graphic": ["own_af_white_tee", "own_af_tee_grey"],
  "Linen layers": ["own_af_white_tee", "own_af_tee_grey"],
  "Pinstripe & graphic": ["own_af_white_tee", "own_af_tee_grey"],
  "Blue linen & olive": ["own_af_white_tee", "own_af_tee_cream"],
  "Graphic & light denim": ["own_af_white_tee", "own_af_tee_grey"],
  "Beach town": ["own_af_white_tee", "own_af_tee_grey"],
  "Harrington & white": ["own_stripe_ls", "own_af_tee_grey"],
  "Sage & brown": ["own_af_white_tee", "own_brown_tee"],
  "Brown linen day": ["own_af_tee_cream", "own_af_white_tee"],
  "Cream & black": ["own_af_tee_grey", "own_af_tee_cream"],
  "Navy zip & khaki": ["own_af_white_tee", "own_af_tee_grey"],
  "Riviera tee": ["own_af_tee_grey"],
  "Summer night tee": ["own_af_tee_cream", "own_af_white_tee"],
  "Day in Porto": ["own_af_white_tee", "own_hotel_tee"],
  "Sage stripes": ["own_af_tee_cream", "own_af_white_tee"],
  "Blue stripes & denim": ["own_af_white_tee", "own_af_tee_grey"],
  "White tee & olive": ["own_af_tee_cream", "own_hotel_tee"],
  "Brown tee & cream": ["own_af_white_tee", "own_hotel_tee"],
  "Grey tee & navy": ["own_af_white_tee", "own_af_tee_cream"],
  "Hotel tee & khaki": ["own_af_white_tee", "own_af_tee_cream"],
  "Cream tee & light denim": ["own_af_white_tee", "own_af_tee_grey"],
  "Sage stripes & linen": ["own_af_tee_cream", "own_af_white_tee"],
  "Navy & cream tank": ["own_af_tank_white", "own_af_tee_cream"],
  "Blue & brown Riviera": ["own_af_tank_white", "own_af_white_tee"],
  "Stripes & navy tank": ["own_af_tank_white", "own_af_white_tee"],
}

# other pieces worth showing under a specific tile: (piece, label, [options])
PIECE_ALT = {
  "Brown linen & taupe cord": [("own_gazelle", "Also great here", ["own_spezial_cream"]), ("own_ms_brown_linen", "Add on top when it cools", ["own_adidas_track_tan", "own_polo_harrington"])],
  "Brown jacket": [("own_midwash", "Daytime option: fresher, more contrast", ["own_lightwash"])],
  "Stripes & sage jacket": [("own_spezial_navy", "Bolder option", ["own_samba_green"])],
  "Seersucker & denim": [("own_midwash", "Also great here: tonal and softer", ["own_af_cream"])],
  "Blue & brown": [("own_arket_blue_heavy", "Also great here: smoother, dressier", ["own_cos_blue"])],
  "Taupe & light blue": [("own_arket_blue_heavy", "Also great here: softer, greyer blue", ["own_cos_blue"])],
  "Black leather & panna cord": [("own_spezial_cream", "Sharper: black shoes", ["shoe_premiata_allblack"])],
  "Waxed & navy": [("own_arket_navy", "Also great here", ["own_arket_alpaca_brown"])],
  "Striped half-zip": [("own_polo_halfzip", "Upgrade: your preferred half-zip", ["knit_halfzip"]), ("own_polo_halfzip", "Upgrade: add on top", ["jacket_suede_bomber"])],
  "Date night": [("own_polo_halfzip", "Upgrade: your preferred half-zip", ["knit_halfzip"]), ("own_polo_halfzip", "Upgrade: add on top", ["jacket_wool_blouson"])],
  "Camp collar": ("own_af_cream", "Lighter for hot days", ["own_af_linen_baggy"]),
  "Brown linen day": [("own_af_cream", "Lighter for hot days", ["own_af_linen_baggy"]),
                      ("own_af_tank_white", "Even better here", ["tank_cream"])],
  "Brown tee & cream": [("own_af_cream", "Lighter for hot days", ["own_af_linen_baggy"]), ("own_brown_tee", "Add on top when it cools down", ["own_brown_jacket_af", "own_adidas_track_tan", "own_cream_cord_jacket"])],
  "Embroidered linen night": ("own_premiata", "Also great here", ["shoe_mexico66"]),
  "Linen layers": ("own_af_tank_white", "Other tank colour", ["tank_navy"]),
  "Blue linen & olive": ("own_af_tank_white", "Other tank colour", ["tank_navy"]),
  "Beach town": [("own_af_tank_white", "Other tank colour", ["tank_cream"])],
  "Sage stripes": ("own_af_tank_white", "Other tank colour", ["tank_cream"]),
  "Sage stripes & linen": [("own_af_tank_white", "Other tank colour", ["tank_cream"])],
  "Blue stripes & denim": ("own_af_tank_white", "Other tank colour", ["tank_navy"]),
  "Granny squares": ("own_af_tank_white", "Even better here", ["tank_cream"]),
  "Sage crochet": ("own_af_tank_white", "Even better here", ["tank_cream"]),
  "Knit polo & white jeans": ("own_spezial_navy", "Timeless option", ["shoe_premiata"]),
  "Blue & cream": [("own_spezial_navy", "Timeless option", ["shoe_premiata"]), ("own_arket_blue_heavy", "Upgrade: add on top", ["jacket_suede_bomber"]), ("own_arket_blue_heavy", "Also great here: smoother, greyer blue", ["own_cos_blue"])],
  "Harrington & white": ("own_spezial_cream", "Other shoes to try", ["shoe_premiata_cream", "shoe_mexico66", "shoe_gg_navy"]),
  "Black knit & cream": ("own_spezial_cream", "Other shoes to try", ["shoe_premiata_cream", "shoe_premiata_black", "shoe_gg_black"]),
  "Houndstooth & green": ("own_samba_green", "Calmer option", ["shoe_diadora_cord"]),
  "Blue cable & grey": ("own_blue_cable", "Upgrade: add on top", ["jacket_suede_bomber"]),
  "Tonal brown": ("own_aircloud_brown", "Upgrade for dry days", ["jacket_wool_blouson"]),
  "Tonal grey": ("own_aircloud_brown", "Upgrade for dry days", ["jacket_wool_blouson"]),
  "Grey tee & navy": ("own_af_tee_grey", "Upgrade: add on top", ["own_polo_harrington"]),
  "Cream tee & light denim": ("own_af_tee_cream", "Upgrade: add on top", ["own_sage_jacket"]),
  "Knit & jeans": [("own_cos_cream", "Upgrade: add on top", ["jacket_suede_bomber"]), ("own_cos_cream", "Upgrade: collar showing", ["own_blue_linen"])],
  "Paolo & cream tee": [("own_af_tee_cream", "Other tee colour", ["own_af_tee_black", "own_brown_tee"]), ("own_af_tee_cream", "Upgrade: add on top", ["own_brown_jacket_af"])],
  "Black leather, white tee": [("own_af_white_tee", "Other tee colour", ["own_af_tee_grey", "own_af_tee_black"]), ("own_af_black_pleated", "Also great here", ["own_af_black_jeans"])],
  "All black, textured": [("knit_black_textured", "Softer version", ["own_ymc_grey"]), ("own_af_black_pleated", "Also great here", ["own_af_black_jeans"])],
  "Tonal chocolate": [("own_arket_alpaca_brown", "Smoother option", ["knit_cashmere_brown"]), ("own_af_brown", "Wool upgrade", ["trouser_wool_brown"]), ("own_premiata", "Fully tonal", ["shoe_premiata_browntonal"])],
  "Chocolate leather": [("own_cos_cream", "Lighter for warm days", ["own_af_white_tee"]), ("own_af_brown", "Also great here", ["own_sn_paolo"])],
  "Poker table": [("own_adidas_track_tan", "Other layers", ["own_polo_harrington", "own_navy_zip_knit", "own_brown_jacket_af"]), ("own_spezial_navy", "Warmer option (with the brown barn jacket)", ["own_samba_maroon"])],
  "Embroidered shirt & black": [("own_white_sneakers", "Also great here", ["own_spezial_cream"])],
}

# how to wear the necklaces in each outfit: (where, detail), shown under the chain / pendant tile
NECKLACES = ("own_ix_figaro", "own_sd_pendant")
NECK_WEAR = {
  "Blue knit & graphic": ("Outside", "over the blue knit, so the pendant sits on the wool. The graphic tee stays underneath."),
  "Sunday lunch": ("Outside", "over the chocolate knit, just below the crew neck. Silver shows up well on dark brown."),
  "Sage & brown": ("Outside the tee, inside the jacket", "on the cream tee, framed by the open sage jacket."),
  "Pinstripe & graphic": ("Outside", "both over the tee."),
  "Riviera tee": ("Outside", "over the white tee, at the collarbone."),
  "Camp collar": ("On skin, inside the shirt", "in the open lace collar, with nothing underneath."),
  "Graphic & light denim": ("Outside", "both over the tee."),
  "Summer dinner": ("On skin, inside the shirt", "showing in the collar, with the top two buttons open."),
  "Summer night tee": ("Outside", "both over the grey tee."),
  "White tee & olive": ("Outside", "over the white tee, at the collarbone."),
  "Grey tee & navy": ("Outside", "both over the grey tee."),
  "Sage crochet": ("Outside the tank, inside the polo", "on the white tank, framed by the unbuttoned crochet placket."),
  "Johnny collar & navy": ("On skin, inside the polo", "sitting in the V of the Johnny collar."),
  "Black knit & cream": ("On skin, inside the polo", "in the V of the Johnny collar, where the silver stands out against the black."),
  "Black camp night": ("On skin, inside the shirt", "both in the open camp collar, with nothing underneath."),
  "Sage stripes & linen": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar, like in your mirror photo."),
  "Blue & brown Riviera": ("Outside the tank, inside the shirt", "on the brown tank, framed by the open collar."),
  "Striped half-zip": ("Outside the tee, inside the half-zip", "on the white tee, showing in the open zip."),
  "Zip cardigan": ("Outside the tee, inside the zip knit", "both on the grey tee, framed by the half-open zip."),
  "Studio day": ("Outside", "over the cream knit. The dark pendant stands out on cream."),
  "Overshirt layers": ("Outside the tee, inside the overshirt", "both on the cream tee, framed by the open overshirt."),
  "Check jacket": ("Outside the tee, inside the jacket", "on the brown tee, framed by the open check jacket."),
  "Stripes & brown": ("Outside", "over the striped knit, just below the crew neck."),
  "Brown & burgundy": ("Outside", "over the chocolate knit."),
  "Oasis day": ("Outside", "over the sweatshirt."),
  "Date night": ("On skin, inside the half-zip", "in the open zip, unzipped to about mid-chest."),
  "Black puffer, done right": ("Outside the knit, inside the puffer", "on the grey knit. Wear the puffer open so it shows."),
  "Embroidered linen night": ("On skin, inside the shirt", "in the open collar, with the top two buttons undone."),
  "Navy terry Riviera": ("On skin, inside the shirt", "in the open collar, with the top buttons undone."),
  "Blue linen & olive": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
  "Beach town": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
  "Blue stripes & denim": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
  "Check & navy": ("Outside the knit, inside the jacket", "over the navy knit, framed by the open check jacket."),
  "Cream & black": ("Outside the tee, inside the jacket", "on the white tee, framed by the open cord jacket."),
  "Brown & grey": ("Outside the knit, inside the jacket", "over the cream knit, framed by the open barn jacket."),
  "Varsity": ("Outside the tee, inside the jacket", "on the cream tee, framed by the open varsity jacket."),
  "Tonal brown": ("Outside the knit, inside the puffer", "over the cream jumper. Wear the puffer open so it shows."),
  "Waxed & cream cord": ("Outside the knit, inside the jacket", "over the cream knit. Wear the jacket open so it shows."),
  "Seersucker & denim": ("On skin, inside the shirt", "in the open collar of the seersucker shirt."),
  "Houndstooth & green": ("Outside the tee, inside the jacket", "on the cream tee, framed by the open Harrington."),
  "Burgundy cord": ("Outside the tee, inside the jacket", "on the grey tee, framed by the open cord jacket."),
  "Blue runner day": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
  "Sage stripes & khaki": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
  "Paolo & cream tee": ("Outside the tee", "at the collar, at your usual 45 cm."),
  "Brown linen & taupe cord": ("On skin, in the open collar", "over the tank, framed by the open collar of the brown shirt."),
  "Black leather & ice denim": ("Outside the tee", "at the collar, at your usual 45 cm, framed by the open jacket."),
  "Black leather & panna cord": ("Outside the tee", "at the collar, at your usual 45 cm, framed by the open jacket."),
  "Black leather & grey tee": ("Outside the tee", "at the collar, at your usual 45 cm, framed by the open jacket."),
  "Black leather, white tee": ("Outside the tee, inside the jacket", "on the white tee at the collar, at your usual 45 cm."),
  "Poker table": ("Outside the tee", "at the collar, at your usual 45 cm. Keep it still: playing with a chain at the table is a tell."),
  "Embroidered shirt & black": ("On skin, inside the shirt", "in the open collar, with the top two buttons undone."),
  "Black polo & pinstripe": ("On skin, inside the polo", "in the V of the Johnny collar, where the silver stands out against the black."),
  "Blue linen & pinstripe": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
  "Brown linen & pinstripe": ("Outside the tank, inside the shirt", "on the white tank, framed by the open collar."),
}

# other jackets to try on in the mirror (owned first; same colour family and warmth)
OUTER_ALT = {
  "AirCloud & cable": ["own_brown_puffer", "own_cos_waxed"],
  "Tonal brown": ["own_brown_puffer", "own_brown_jacket_af"],
  "Brown puffer": ["own_aircloud_brown", "own_cos_waxed"],
  "Cold street": ["own_aircloud_brown", "own_cos_waxed"],
  "Black puffer, done right": ["own_md_leather"],
  "Black puffer & burgundy": ["own_brown_puffer", "own_aircloud_brown"],
  "Puffer vest": ["own_polo_harrington", "own_aircloud_brown"],
  "Varsity": ["own_brown_jacket_af", "own_polo_harrington"],
  "Rainy day": ["own_brown_jacket_af", "own_brown_puffer"],
  "Brown jacket": ["own_cos_waxed", "own_brown_puffer"],
  "Check jacket": ["own_brown_jacket_af"],
  "Check & navy": ["own_brown_jacket_af", "own_brown_puffer"],
  "Navy harrington": ["own_brown_jacket_af", "own_sage_jacket"],
  "Harrington & white": ["own_sage_jacket", "own_brown_jacket_af"],
  "Sage & brown": ["own_cream_cord_jacket", "own_polo_harrington"],
  "Stripes & sage jacket": ["own_polo_harrington", "own_cream_cord_jacket"],
  "Cream cord & Eagles": ["own_sage_jacket", "own_brown_jacket_af"],
  "Cream & black": ["own_sage_jacket"],
  "Cord jacket & stripes": ["own_brown_jacket_af", "own_sage_jacket"],
  "Waxed & navy": ["own_brown_jacket_af"],
  "Waxed & cream cord": ["own_brown_puffer", "own_brown_jacket_af"],
  "Brown & grey": ["own_check_jacket", "own_cream_cord_jacket"],
  "Taupe & light blue": ["own_aircloud_brown", "own_polo_harrington"],
  "Tonal grey": ["own_brown_puffer", "own_brown_jacket_af"],
}

VIBE = {
  "Knit & jeans": ("In between", "Everyday"),
  "Brown jacket": ("Street", "Weekend"),
  "Knit polo": ("Classy", "Lunch / drinks"),
  "Night out": ("Classy", "Night out"),
  "Striped half-zip": ("In between", "Everyday"),
  "Zip cardigan": ("Street", "Everyday"),
  "Cream & brown": ("Classy", "Dinner"),
  "Studio day": ("In between", "Everyday"),
  "Guinness, upgraded": ("Street", "Weekend"),
  "Brown puffer": ("In between", "Everyday"),
  "Puffer vest": ("In between", "Weekend"),
  "Varsity": ("Street", "Weekend"),
  "Date night": ("Classy", "Date / night out"),
  "Grey on black": ("Classy", "Dinner"),
  "Rainy day": ("In between", "Rainy day"),
  "Cold street": ("Street", "Weekend"),
  "Coffee run": ("Street", "Weekend daytime"),
  "Club tee": ("Street", "Warm day"),
  "Knit polo & white jeans": ("Classy", "Lunch / date"),
  "Blue knit & graphic": ("Street", "Everyday"),
  "Weekend hoodie": ("Street", "Weekend"),
  "Rugby & navy": ("In between", "Daytime"),
  "Sunday lunch": ("Classy", "Family lunch"),
  "Overshirt layers": ("Street", "Everyday"),
  "Check jacket": ("In between", "Everyday / work"),
  "Collar & crew": ("Classy", "Dinner / work"),
  "Sweatshirt & white denim": ("Street", "Everyday"),
  "Oxford & stone": ("In between", "Lunch / work"),
  "Stripes & brown": ("In between", "Everyday"),
  "Black puffer, done right": ("Street", "Everyday"),
  "Linen layers": ("In between", "Warm day"),
  "Navy & white": ("Classy", "Dinner outside"),
  "Pinstripe & graphic": ("Street", "Warm day"),
  "Stripes & sage jacket": ("In between", "Everyday"),
  "AirCloud & cable": ("In between", "Everyday"),
  "Navy harrington": ("Classy", "Lunch / dinner"),
  "Cream cord & Eagles": ("Street", "Weekend"),
  "Coastal & navy": ("In between", "Everyday"),
  "Oasis day": ("Street", "Weekend"),
  "Blue cable & grey": ("In between", "Everyday"),
  "Cord jacket & stripes": ("In between", "Everyday"),
  "Harrington & white": ("In between", "Daytime"),
  "Sage & brown": ("In between", "Daytime"),
  "Navy zip & khaki": ("Classy", "Dinner / work"),
  "Seersucker & denim": ("Street", "Holiday / daytime"),
  "Sage stripes": ("In between", "Daytime"),
  "Blue stripes & denim": ("Street", "Weekend"),
  "Brown linen day": ("In between", "Daytime"),
  "Blue & brown": ("In between", "Everyday / dinner"),
  "Check & navy": ("In between", "Everyday"),
  "Brown & burgundy": ("Street", "Weekend"),
  "Tonal brown": ("Classy", "Dinner / date"),
  "Black puffer & burgundy": ("Street", "Everyday"),
  "Blue & cream": ("In between", "Daytime"),
  "Cowboys & khaki": ("Street", "Weekend"),
  "Riviera tee": ("In between", "Holiday / lunch"),
  "Camp collar": ("Street", "Warm day"),
  "Blue linen & olive": ("In between", "Daytime"),
  "Graphic & light denim": ("Street", "Weekend"),
  "Summer dinner": ("Classy", "Dinner"),
  "Summer night tee": ("In between", "Night out"),
  "Beach town": ("Street", "Holiday"),
  "Khaki & blue": ("In between", "City day"),
  "Day in Porto": ("Street", "Daytime"),
  "Granny squares": ("Street", "Weekend"),
  "Sage crochet": ("In between", "Daytime"),
  "Johnny collar & navy": ("Classy", "Dinner"),
  "Black knit & cream": ("In between", "Evening"),
  "Black camp night": ("In between", "Night out"),
  "White tee & olive": ("Street", "Daytime"),
  "Brown tee & cream": ("Street", "Weekend"),
  "Grey tee & navy": ("In between", "Evening"),
  "Hotel tee & khaki": ("Street", "Weekend"),
  "Cream tee & light denim": ("Street", "Everyday"),
  "Cream & black": ("Street", "Weekend"),
  "Blue on black": ("Classy", "Dinner"),
  "Waxed & navy": ("Classy", "Lunch / city"),
  "Waxed & cream cord": ("In between", "Rainy weekend"),
  "Navy & taupe cord": ("Street", "Weekend"),
  "Brown & grey": ("Classy", "Lunch / dinner"),
  "Taupe & light blue": ("In between", "Everyday"),
  "Tonal grey": ("In between", "Weekend"),
  "Embroidered linen night": ("Classy", "Summer dinner"),
  "Checkerboard knit": ("In between", "Winter weekend"),
  "Navy terry Riviera": ("Classy", "Holiday dinner"),
  "Chocolate coat": ("Classy", "Dinner / city"),
  "Sage stripes & linen": ("In between", "Daytime / holiday"),
  "Navy & cream tank": ("Street", "Weekend"),
  "Blue & brown Riviera": ("Classy", "Holiday dinner"),
  "Stripes & navy tank": ("Classy", "Lunch / dinner"),
  "Country dinner": ("Classy", "Relaxed dinner"),
  "Houndstooth & green": ("In between", "Weekend"),
  "Burgundy cord": ("Street", "Weekend"),
  "Pink stripe night": ("Street", "Night out"),
  "Blue runner day": ("In between", "Daytime"),
  "Sage stripes & khaki": ("In between", "Evening out"),
  "Paolo & cream tee": ("In between", "Weekend / city day"),
  "Brown linen & taupe cord": ("In between", "Spring / autumn day"),
  "Black leather & grey": ("In between", "Night out / city"),
  "Black leather & ivory": ("In between", "Night out / city"),
  "Black leather & ice denim": ("Street", "City day / evening"),
  "Black leather & panna cord": ("In between", "Dinner / city"),
  "Slate blue & navy": ("Classy", "Dinner"),
  "Black leather & slate blue": ("In between", "City / evening"),
  "Black leather & grey tee": ("Street", "Travel day / show night"),
  "Black leather, white tee": ("In between", "Night out / dinner"),
  "All black, textured": ("In between", "Night out"),
  "Tonal chocolate": ("Classy", "Dinner / city"),
  "Chocolate leather": ("Classy", "Dinner / night out"),
  "Poker table": ("In between", "Casino / poker night"),
  "Embroidered shirt & black": ("Classy", "Day out / dinner"),
  "Black polo & pinstripe": ("Classy", "Summer evening"),
  "Blue linen & pinstripe": ("In between", "Lunch / day out"),
  "Brown linen & pinstripe": ("In between", "Daytime"),
}

OWNED_INFO = json.load(open(os.path.join(HERE, "owned.json"))) if os.path.exists(os.path.join(HERE, "owned.json")) else {}

SEASON_INFO = {
  "Special occasions": ("For a special day", "One standout piece, the rest from your wardrobe", "The outfits above are your fundamentals. These go a step further: each is built around one piece from a modern, young brand that sets you apart, while staying classy."),
  "Spring": ("March – May", "Mornings 7–10 °C, afternoons 16–22 °C", "Showers are common (about 110–120 mm a month), so bring a light jacket you can take off."),
  "Summer": ("June – September", "Mornings 13–16 °C, afternoons 24–28 °C, heatwaves 32–35 °C+", "Dry July and August. Evenings cool down, so a light layer helps. September is still warm."),
  "Autumn": ("October – November", "Mornings 8–12 °C, afternoons 15–21 °C", "The rain comes back hard (about 160–175 mm a month). Knits and jackets, and suede on dry days only."),
  "Winter": ("December – February", "Mornings 3–6 °C (some frost), afternoons 11–14 °C", "The wettest months in Braga (about 170–220 mm a month). Puffers, warm knits and leather shoes for rainy days."),
}

KNOWN_FRONT = {}
LAYER_NOTE = ' <b>Necklaces, layered:</b> IX figaro at 46 cm, with your Serge DeNimes pendant hooked on the last ring of its chain (about 52 cm), so they sit about 6 cm apart.'
MY_FRONT = 142  # his ASOS round pair, measured hinge to hinge
ALT_SLOTS = ("alt", "alt2", "alt3", "alt4", "alt5", "alt6", "alt7", "alt8")
MAIN_BRANDS = ("Abercrombie", "COS", "Les Deux", "Arket")

def sorted_alts(slot):
    """Alternatives with the main brands (A&F, COS, Les Deux, Arket) listed first."""
    alts = [slot[k] for k in ALT_SLOTS if slot.get(k)]
    return sorted(alts, key=lambda a: not any(a.get("brand", "").startswith(b) for b in MAIN_BRANDS))

# layered necklace pairs: (name, vibe, short piece url, short length cm, long piece url, long length cm, note)
PAIRS = [
  ("Budget try-out", "In between", "https://ixstudioscph.com/products/ix-figaro-chain-silver", "50", "https://kiama.pt/produto/colar-com-cruz/", "60",
   "A fine figaro plus a brushed cross made in Portugal. The cheapest way to find out if you like layering before spending more."),
  ("Portuguese pair", "In between", "https://hattonlabs.com/products/silver-twisted-rope-chain-m", "51", "https://kiama.pt/produto/colar-vieira-de-santiago/", "60",
   "A twisted rope chain with the Camino scallop shell lower down. Atlantic-coast and personal, great with a linen shirt open at the collar."),
  ("Riviera anchor", "In between", "https://ixstudioscph.com/products/ix-figaro-chain-silver", "50", "https://www.werkstatt-muenchen.com/products/chain-mini-anchor", "64",
   "Fine figaro at the collarbone and a tiny anchor further down. Nautical without being literal, perfect for summer."),
  ("Old-money medal", "Classy", "https://ixstudioscph.com/products/ix-figaro-chain-silver", "46", "https://sergedenimes.com/products/silver-st-christopher-necklace", "52",
   "A fine figaro close to the neck with the St Christopher just below. The most classic pair here, very Ralph Lauren."),
  ("Mariner & laurel", "In between", "https://ixstudioscph.com/products/ix-curb-marina-chain-silver", "45", "https://sergedenimes.com/products/silver-laurel-necklace", "52",
   "Preppy anchor links close to the neck with a small laurel medal below. Good with a knit polo or a rugby collar open."),
  ("Matches your bracelet", "Street", "https://www.allblues.se/product/cuban-necklace-silver", "47", "https://www.allblues.se/product/coin-pendant-01-large", "54",
   "The same 4 mm Cuban as your All Blues bracelet, with their coin below. One brand, so all the silver is identical."),
  ("Copenhagen", "Classy", "https://www.tomwoodproject.com/en-eu/products/billie-chain", "46", "https://www.tomwoodproject.com/en-eu/products/umi-pendant", "52",
   "Paperclip chain plus a plain polished tag. Minimal and Scandinavian, the investment pair. The bright polish matches your Rolex bezel.", 340),
]

def all_for_role(role):
    seen, out = set(), []
    for f in sorted(os.listdir(HERE)):
        if f.startswith("products_") and f.endswith(".json"):
            for q in json.load(open(os.path.join(HERE, f))):
                if q.get("role") == role and q.get("image_url"):
                    u = q.get("url", "").split("?")[0]
                    if u and u not in seen:
                        seen.add(u); out.append(q)
    return out

def load_products():
    prod = {}
    entries = []
    for f in sorted(os.listdir(HERE)):
        if f.startswith("products_") and f.endswith(".json"):
            entries += json.load(open(os.path.join(HERE, f)))
    direct = [p for p in entries if p.get("role") in ROLE_INFO and not p.get("lookbook_only")]
    aliased = [dict(p, role=ALIAS[p["role"]], rank="alt") for p in entries if p.get("role") in ALIAS]
    for p in direct + aliased:
        if p["role"].startswith("shoe_") and any(b in p.get("brand", "") for b in BLOCK_BRANDS_SHOES):
            continue
        slot = prod.setdefault(p["role"], {})
        if any(q.get("url", "").split("?")[0] == p.get("url", "").split("?")[0] for q in slot.values()):
            continue
        rank = p.get("rank", "primary")
        if rank in slot:
            rank = next((k for k in ALT_SLOTS if k not in slot), None)
            if rank is None:
                continue
        slot[rank] = p
    for r, slot in prod.items():
        if "primary" not in slot:
            for k in ("alt", "alt2", "alt3"):
                if k in slot:
                    slot["primary"] = slot.pop(k); break
    return prod

def money(x):
    try:
        x = float(x)
    except Exception:
        return ""
    return f"€{x:,.0f}" if x == int(x) else f"€{x:,.2f}"

def tile(key, prod, swap=""):
    if key in OWNED:
        cat, label = OWNED[key]
        info = OWNED_INFO.get(key)
        if info and info.get("image_url", "").startswith("img/"):
            import base64
            fp = os.path.join(os.path.dirname(OUT), info["image_url"])
            if os.path.exists(fp):
                info = dict(info, image_url="data:image/jpeg;base64," + base64.b64encode(open(fp, "rb").read()).decode())
        if info and info.get("image_url"):
            note = "" if info.get("match") == "exact" else '<div class="pr">Closest match to yours</div>'
            return f'''<div class="tile owned-img" data-key="{key}" data-cat="{e(cat)}"><a class="ph" href="{e(info["url"])}" target="_blank" rel="noopener">
<em class="owntag">✓ You have it</em><img loading="lazy" referrerpolicy="no-referrer" src="{e(info["image_url"])}" alt="{e(label)}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(label)}</span></a>
<div class="meta"><div class="br">{e(info.get("brand",""))}</div><div class="nm">{e(label)}</div>{note}{swap}</div></div>'''
        return f'''<div class="tile owned" data-key="{key}" data-cat="{e(cat)}"><div class="ph"><em class="owntag">✓ You have it</em><span>{e(label)}</span></div>
<div class="meta"><div class="nm">{e(label)}</div></div></div>'''
    p = prod.get(key, {}).get("primary")
    cat, label = ROLE_INFO[key]
    if not p:
        return ""
    alts = sorted_alts(prod[key])
    alt_html = "".join(f'<a class="alt" href="{e(a["url"])}" target="_blank" rel="noopener">or {e(a["brand"])} · {money(a.get("price_eur"))}</a>' for a in alts)
    return f'''<div class="tile" data-key="{key}" data-cat="{e(cat)}"><a class="ph" href="{e(p["url"])}" target="_blank" rel="noopener">
<img loading="lazy" referrerpolicy="no-referrer" src="{e(p.get("image_url",""))}" alt="{e(p["name"])}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(label)}</span></a>
<div class="meta"><div class="br">{e(p["brand"])}</div><a class="nm" href="{e(p["url"])}" target="_blank" rel="noopener">{e(p["name"])}</a>
<div class="pr">{money(p.get("price_eur"))}{' · ' + e(p.get("colour","")) if p.get("colour") else ''}</div>{alt_html}{swap}</div></div>'''

ALT_HINT = {
  "own_aircloud_brown": "warmer, more vibrant brown",
  "own_brown_puffer": "deeper, darker brown, bulkier and warmer",
  "own_cos_waxed": "khaki and chocolate waxed cotton, for mild rain",
  "own_brown_jacket_af": "dark coffee, lighter weight",
  "own_cream_cord_jacket": "light stone corduroy",
  "own_sage_jacket": "light sage",
  "own_polo_harrington": "navy",
}
TREND_TAG = {
  "shoe_premiata_cream": ("More timeless", "Vintage tennis shape, not tied to any trend wave."),
  "shoe_mexico66": ("Timeless design, trend at its peak", "A 1966 classic, but the slim-sneaker wave is at its height now. It will cool off, and the shoe will still look right."),
  "shoe_premiata_black": ("In between", "Terrace shape like your Spezials, a wave that's past its peak, but the quiet brand ages slower."),
  "shoe_gg_navy": ("More trendy, late stage", "Golden Goose peaked around 2018–22. Still everywhere, and the distressed look is starting to read dated."),
  "shoe_gg_black": ("More trendy, late stage", "The most recognisable Golden Goose, so it says \"trend\" the loudest. Past its peak."),
}
INNER_PRIORITY = ["own_af_tank_white", "tank_cream", "tank_navy", "tank_brown", "own_af_white_tee", "own_af_tee_grey", "own_af_tee_cream", "own_af_tee_black", "own_hotel_tee", "own_brown_tee",
                  "own_stripe_ls", "shirt_oxford", "own_blue_linen"]

def piece_view(k, prod):
    """(image, link, title, subtitle) for any owned key or shop role."""
    import base64
    if k in OWNED:
        info = OWNED_INFO.get(k, {})
        img = info.get("image_url", "")
        if img.startswith("img/"):
            fp = os.path.join(os.path.dirname(OUT), img)
            img = ("data:image/jpeg;base64," + base64.b64encode(open(fp, "rb").read()).decode()) if os.path.exists(fp) else ""
        sub = ALT_HINT.get(k) or info.get("colour", "")
        return img, info.get("url", "#"), OWNED[k][1], sub
    p = prod.get(k, {}).get("primary") or {}
    sub = (ALT_HINT.get(k) or p.get("colour", "")) + " · " + money(p.get("price_eur")) + ", to buy"
    return p.get("image_url", ""), p.get("url", "#"), (p.get("brand", "") + " " + p.get("name", "")).replace("Abercrombie & Fitch", "A&F"), sub

def swap_box(kind, alts, prod):
    views = [piece_view(k, prod) for k in alts]
    short = " · ".join(v[2].replace("Your ", "your ") for v in views)
    items = ""
    for k, (img, u, t, sub) in zip(alts, views):
        pic = ('<img loading="lazy" referrerpolicy="no-referrer" src="' + e(img) + '" alt="">') if img else ""
        tag = ('<i class="trend">' + e(TREND_TAG[k][0]) + '</i><small>' + e(TREND_TAG[k][1]) + '</small>') if k in TREND_TAG else ""
        items += '<a class="swapitem" href="' + e(u) + '" target="_blank" rel="noopener"><span class="swapph">' + pic + '</span><b>' + e(t) + '</b><small>' + e(sub) + '</small>' + tag + '</a>'
    return '<details class="swapbox"><summary><span class="swaplab">' + kind + ':</span> ' + e(short) + '</summary><div class="swapgrid">' + items + '</div></details>'

def swaps_for(name, pieces, prod):
    """Which tile gets which swap box: backup inner layer, and other jackets to try."""
    out = {}
    if name in INNER_ALT:
        inner = next((k for k in INNER_PRIORITY if k in pieces), None)
        if inner:
            out[inner] = swap_box("Backup if it's in the wash" if inner in OWNED else "Until you buy it", INNER_ALT[name], prod)
    if name in PIECE_ALT:
        entries = PIECE_ALT[name]
        for piece, label, alts in (entries if isinstance(entries, list) else [entries]):
            if piece in pieces:
                out[piece] = out.get(piece, "") + swap_box(label, alts, prod)
    if name in OUTER_ALT:
        outer = next((k for k in pieces if (ROLE_INFO.get(k) or OWNED.get(k))[0] == "Outerwear"), None)
        if outer:
            out[outer] = out.get(outer, "") + swap_box("Other jacket to try", OUTER_ALT[name], prod)
    worn = [k for k in NECKLACES if k in pieces]
    if worn:
        if name not in NECK_WEAR:
            print("WARNING: no necklace wear note for", name)
        else:
            where, how = NECK_WEAR[name]
            for k in worn:
                extra = ""
                if len(worn) == 2:
                    extra = " Figaro at 46 cm." if k == "own_ix_figaro" else " Hooked on the figaro's last ring, about 6 cm lower."
                out[k] = f'<div class="wearhow"><span>How to wear it</span><b>{e(where)}.</b> {e(how[:1].upper() + how[1:])}{extra}</div>' + out.get(k, "")
    return out

def build():
    global OUTFITS
    if NO_CAPS:
        OUTFITS = [(a, b, c, d, [k for k in pcs if k not in ("own_cap_navy", "cap_ald_yankees")]) for a, b, c, d, pcs in OUTFITS]
    prod = load_products()
    usage = Counter(k for *_, pieces in OUTFITS for k in pieces if k in ROLE_INFO and prod.get(k, {}).get("primary"))
    seasons = ["Spring", "Summer", "Autumn", "Winter", "Special occasions"]
    sid = {s: s.lower().replace(" ", "-") for s in seasons}
    sid["Special occasions"] = "special"
    order = ["Spring", "Summer", "Autumn", "Winter"]
    special = sorted([o for o in OUTFITS if o[0].startswith("Special ")], key=lambda o: order.index(o[0].split(" ", 1)[1]))
    sec = []
    n = 0
    outfit_num = {}
    for s in seasons:
        cards = []
        for season, name, inspo, note, pieces in (special if s == "Special occasions" else OUTFITS):
            if s != "Special occasions" and season != s:
                continue
            n += 1
            outfit_num[name] = n
            sw = swaps_for(name, pieces, prod)
            tiles = "".join(tile(k, prod, sw.get(k, "")) for k in sorted(pieces, key=lambda k: CATS.index((ROLE_INFO.get(k) or OWNED.get(k))[0])))
            total = sum(float(prod[k]["primary"].get("price_eur") or 0) for k in pieces if k in ROLE_INFO and prod.get(k, {}).get("primary"))
            hero = False
            n_own = sum(1 for k in pieces if k in OWNED)
            n_all = sum(1 for k in pieces if k in OWNED or prod.get(k, {}).get("primary"))
            vibe, occ = VIBE.get(name, ("In between", "Everyday"))
            vcls = {"Street": "v-street", "In between": "v-mid", "Classy": "v-classy"}[vibe]
            cards.append(f'''<article id="o{n}" class="card{' hero' if hero else ''}" data-name="{e(name)}" data-vibe="{vcls}" data-ready="{'yes' if n_all and n_own == n_all else ('one' if n_all - n_own == 1 else 'no')}">{'<div class="herotag">Your reference look</div>' if hero else ''}<header><span class="num">{n:02d}</span><div><h3>{e(name)}</h3>
<p class="inspo"><span class="vchip {vcls}">{e(vibe)}</span>{('<span class="ochip">' + e(season.split(" ", 1)[1]) + '</span>') if season.startswith("Special ") else ""}<span class="ochip">{e(occ)}</span>{e(inspo)}</p></div><span class="tots"><button class="fav" type="button" aria-pressed="false" aria-label="Save to favourites">☆ Favourite</button><button class="cmp" type="button" aria-pressed="false" aria-label="Add to compare">＋ Compare</button><span class="ownchip">You own {n_own} of {n_all}</span><span class="tot">{("New pieces: " + money(total)) if total else "All pieces you own"}</span></span></header>
<p class="note">{e(note)}{LAYER_NOTE if "own_ix_figaro" in pieces and "own_sd_pendant" in pieces else ""}</p><div class="tiles">{tiles}</div></article>''')
        si = SEASON_INFO.get(s)
        info = f'<div class="season"><span class="months">{e(si[0])}</span><span class="temps">{"" if s == "Special occasions" else "Braga: "}{e(si[1])}</span><span class="tip">{e(si[2])}</span></div>' if si else ""
        sec.append(f'<section id="{sid[s]}"><h2>{e(s)}</h2>{info}{"".join(cards)}</section>')

    # sunglasses lookbook
    sg = all_for_role("sunglasses")
    OWNED_URLS = {v.get("url", "").split("?")[0] for v in OWNED_INFO.values()}
    def fw(q):
        v = str(q.get("front_width_mm") or KNOWN_FRONT.get(q.get("name"), "")).strip()
        return v
    def fit_badge(v):
        import re as _re
        m = _re.search(r"\d+(?:\.\d+)?", v or "")
        if not m:
            return '<div class="fitb fb-unk">Size unknown: compare on the shop page</div>'
        d = float(m.group()) - MY_FRONT
        est = " (estimate)" if "~" in v or "est" in v else ""
        if abs(d) <= 3: return f'<div class="fitb fb-ok">✓ Fits like yours{est}</div>'
        if 3 < d <= 6: return f'<div class="fitb fb-mid">A bit bigger than yours{est}</div>'
        if -6 <= d < -3: return f'<div class="fitb fb-mid">A bit smaller than yours{est}</div>'
        return f'<div class="fitb fb-far">{"Much bigger" if d > 0 else "Much smaller"} than yours{est}</div>'
    sg_cards = "".join(f'''<div class="sg"><a class="ph" href="{e(q["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(q["image_url"])}" alt="{e(q["name"])}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(q["brand"])}</span></a>
<div class="meta"><div class="br">{e(q["brand"])}</div><a class="nm" href="{e(q["url"])}" target="_blank" rel="noopener">{e(q["name"])}</a>
<div class="pr">{money(q.get("price_eur"))}{" · " + e(q.get("shape","")) if q.get("shape") else ""}</div>
<div class="pr">{e(q.get("colour",""))}{(" · Size " + e(q["size"])) if q.get("size") else ""}</div>
<div class="fwid">{("Front width: " + e(fw(q)) + " mm") if fw(q) else "Front width: check the product page"}</div>{fit_badge(fw(q))}{'<div class="fitb fb-ok">✓ You have this pair</div>' if q.get("url", "").split("?")[0] in OWNED_URLS else ""}
<div class="why">{e(q.get("fit_note",""))}</div></div></div>''' for q in sorted(sg, key=lambda q: float(q.get("price_eur") or 0)))
    # necklace lookbook
    TYPE_OF = {"jewelry_chain": "thin chain", "necklace_chain_bold": "bold chain", "necklace_pendant": "pendant"}
    neck = [dict(q, type=q.get("type") or ("pendant" if "pendant" in q["name"].lower() else TYPE_OF[r])) for r in TYPE_OF for q in all_for_role(r)] + all_for_role("necklace_lookbook")
    seen_u, neck2 = set(), []
    for q in neck:
        u = q["url"].split("?")[0]
        if u not in seen_u: seen_u.add(u); neck2.append(q)
    def nk_card(q):
        sale = ' <span class="start">On sale</span>' if q.get("on_sale") else ""
        spec = " · ".join(x for x in [("Width: " + e(str(q["width_mm"])) + (" mm" if str(q.get("width_mm","")).replace(".","").isdigit() else "")) if q.get("width_mm") else "", ("Lengths: " + e(str(q["lengths_cm"])) + " cm") if q.get("lengths_cm") else ""] if x)
        return f'''<div class="sg"><a class="ph" href="{e(q["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(q["image_url"])}" alt="{e(q["name"])}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(q["brand"])}</span></a>
<div class="meta"><div class="br">{e(q["brand"])}</div><a class="nm" href="{e(q["url"])}" target="_blank" rel="noopener">{e(q["name"])}</a>
<div class="pr">{money(q.get("price_eur"))}{sale}</div><div class="pr">{e(q.get("colour",""))}</div>
{('<div class="fwid">' + spec + '</div>') if spec else ''}<div class="why">{e(q.get("fit_note",""))}</div></div></div>'''
    groups = [("Symbols that are you", "atlas", "Sisyphus and his stone (Camus), Atlas carrying the world (Atlas Shrugged), the armillary sphere (Portugal's flag), and the Stoic and Greek ideas from your own notes."), ("Thin chains", "thin chain", "1.5–2.5 mm. Everyday, quiet, sits under an open collar."), ("Bolder chains", "bold chain", "3–5 mm. More presence, best with tees, knits and street days."), ("Pendants", "pendant", "A small cross, coin or medallion on a fine chain. The most personal option."), ("Ready-made layered sets", "layered set", "Two strands sold as one piece, already spaced for you.")]
    nk_html = "".join(f'''<h3 class="cat">{e(g)} <span class="muted" style="font-weight:400;font-size:14px">— {e(d)}</span></h3><div class="sgrid">{"".join(nk_card(q) for q in sorted([q for q in neck2 if q["type"]==t], key=lambda q: float(q.get("price_eur") or 0)))}</div>''' for g,t,d in groups if any(q["type"]==t for q in neck2))
    by_url = {q["url"].split("?")[0]: q for q in neck2}
    def pair_card(name, vibe, su, sl, lu, ll, note, sp=None, lp=None):
        a, b = by_url.get(su.split("?")[0]), by_url.get(lu.split("?")[0])
        if not a or not b:
            print("pair skipped (missing piece):", name); return ""
        vcls = {"Street": "v-street", "In between": "v-mid", "Classy": "v-classy"}[vibe]
        half = lambda q, tag, ln: f'''<a class="ph" href="{e(q["url"])}" target="_blank" rel="noopener"><em class="lentag">{tag} · {e(ln)} cm</em><img loading="lazy" referrerpolicy="no-referrer" src="{e(q["image_url"])}" alt="{e(q["name"])}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(q["brand"])}</span></a>'''
        line = lambda q, tag, ln, pr: f'<div class="pr"><b>{tag} ({e(ln)} cm):</b> <a href="{e(q["url"])}" target="_blank" rel="noopener">{e(q["brand"])} {e(q["name"])}</a> · {money(pr)}</div>'
        pa, pb = sp or a.get("price_eur") or 0, lp or b.get("price_eur") or 0
        tot = float(pa) + float(pb)
        return f'''<div class="pair"><div class="pairimgs">{half(a, "Short", sl)}{half(b, "Long", ll)}</div>
<div class="meta"><div class="pairhd"><b>{e(name)}</b><span class="vchip {vcls}">{e(vibe)}</span><span class="tot">Together: {money(tot)}</span></div>
{line(a, "Short", sl, pa)}{line(b, "Long", ll, pb)}<div class="why">{e(note)}</div></div></div>'''
    pairs_html = "".join(pair_card(*p) for p in PAIRS)
    if pairs_html:
        nk_html = f'''<h3 class="cat">Layered pairs <span class="muted" style="font-weight:400;font-size:14px">— two necklaces worn together, one shorter and one longer</span></h3>
<div class="fit"><ul><li><b>Leave about 5 cm between them</b> (for you: 50 + 55 cm, or 50 + 60 cm for a pendant over a knit) so they don't tangle and each one shows.</li>
<li><b>Mix the textures, keep the metal.</b> A plain chain plus a pendant, or a thin chain plus a bolder one. All silver, to match your Rolex.</li>
<li><b>The longer one carries the detail.</b> Put the pendant or the bolder chain on the long strand and keep the short one quiet.</li>
<li><b>Best with</b> a tee, an open collar or a crewneck knit. With a buttoned shirt, wear just one.</li></ul></div>
<div class="pgrid">{pairs_html}</div>''' + nk_html
    nk_section = f'''<section id="necklaces"><h2>Necklaces</h2><p class="lede">All silver-toned to match your Rolex, and sterling silver unless the colour says steel. <b>Length guide for you:</b> 50 cm sits around the collarbone and is the best everyday length for chains; 55 cm sits a little lower and works well for pendants and over knits. Wear one on its own, or layer two (see Layered pairs below).</p>{nk_html}</section>'''
    sg_section = f'''<section id="sunglasses"><h2>Sunglasses</h2><p class="lede">All the frames side by side, cheapest first. Your ASOS round pair in clear lilac fits you well and measures <b>142 mm</b> across the front (hinge to hinge). Each frame below is marked against it: <b>✓ fits like yours</b> means within 3 mm. Rounded, panto-style shapes in clear or crystal acetate clearly work on you. You now also own the Kaleos Jaconelli in dark havana.</p><div class="sgrid">{sg_cards}</div></section>'''

    # caps lookbook
    caps = all_for_role("cap_structured")
    def cap_card(q):
        return (f'''<div class="sg"><a class="ph" href="{e(q["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(q["image_url"])}" alt="{e(q["name"])}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(q["brand"])}</span></a>
<div class="meta"><div class="br">{e(q["brand"])}{' · <b>Top pick</b>' if q.get("rank")=="main" else ''}</div><a class="nm" href="{e(q["url"])}" target="_blank" rel="noopener">{e(q["name"])}</a>
<div class="pr">{money(q.get("price_eur"))}{' <span class="start">On sale</span>' if q.get("on_sale") else ''}</div><div class="pr">{e(q.get("colour",""))}</div>
<div class="fwid">{e(q.get("construction",""))}</div>{'<div class="fitb fb-ok">✓ Shape very close to yours</div>' if q.get("similarity")=="high" else ('<div class="fitb fb-mid">Close, with one compromise</div>' if q.get("similarity")=="medium" else '')}<div class="why">{e(q.get("fit_note",""))}</div></div></div>''')
    CAP_GROUPS = [("best", "Best fit for you", "A rounded crown and curved brim like your Western, with room for your head."),
                  ("yankees", "If you want the Yankees NY", "The classic white NY on navy, in caps that open wider than the '47."),
                  ("also", "Also good", "More room or a lower price, with one compromise each.")]
    cap_cards = "".join(f'<h3 class="cat">{e(t)} <span class="muted" style="font-weight:400;font-size:14px">— {e(d)}</span></h3><div class="sgrid">' + "".join(cap_card(q) for q in caps if q.get("colour_group") == g) + '</div>' for g, t, d in CAP_GROUPS if any(q.get("colour_group") == g for q in caps))

    cap_section = f'''<section id="caps"><h2>Caps</h2><p class="lede"><b>Replacing the navy cap.</b> Your '47 Base Runner is too small: '47's one-size caps only open to about 57–58 cm, so return it to Asphaltgold by about 27 Oct. Every cap here is navy, opens wider (or comes in real sizes) and has the shape of your A&F Western: a rounded crown that sits deep and a pre-curved brim. <b>Before ordering, measure your head:</b> a tape around the forehead, just above the ears. Up to about 60 cm, everything here fits; over 60 cm, go for the A.P.C. in 60, the Kith × '47 in XL, the ALD Washed Script Chino or the Carhartt. Ranked #1–#8.</p>{cap_cards}</section>''' if caps else ""

    # brands for you
    brands = all_for_role("brand_pick")
    def brand_card(q):
        return f'''<div class="sg"><a class="ph" href="{e(q["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(q["image_url"])}" alt="{e(q["product_name"])}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(q["brand"])}</span></a>
<div class="meta"><div class="br">{e(q["brand"])} · {e(q["country"])}</div><div class="why" style="color:var(--text)">{e(q["why"])}</div>
<div class="pr" style="margin-top:4px">Typical prices {e(q["price_range"])}</div>
<div class="fwid">Try: <a href="{e(q["url"])}" target="_blank" rel="noopener">{e(q["product_name"])}</a>, {e(q["product_colour"])} · {money(q.get("price_eur"))}</div>
<div class="why">Size: {e(q["sizing"])}</div></div></div>'''
    BT = [("affordable", "Affordable"), ("mid", "Mid-range"), ("investment", "Investment pieces")]
    brand_html = "".join(f'<h3 class="cat">{t}</h3><div class="sgrid">' + "".join(brand_card(q) for q in brands if q["tier"] == k) + "</div>" for k, t in BT if any(q["tier"] == k for q in brands))
    # inspiration board
    looks = []
    for f in sorted(os.listdir(HERE)):
        if f.startswith("inspo_") and f.endswith(".json"):
            d = json.load(open(os.path.join(HERE, f)))
            looks += d["looks"] if isinstance(d, dict) else d
    SEASON_ORDER = ["Spring", "Summer", "Autumn", "Winter"]
    looks.sort(key=lambda q: (SEASON_ORDER.index(q.get("season", "Autumn")) if q.get("season") in SEASON_ORDER else 9, q.get("id", "")))
    def look_card(q):
        vcls = {"Street": "v-street", "In between": "v-mid", "Classy": "v-classy"}.get(q.get("vibe", ""), "v-mid")
        pcs = "".join(f"<li>{e(p)}</li>" for p in q.get("pieces", []))
        return (f'''<article class="lk" data-id="{e(q["id"])}" data-season="{e(q.get("season",""))}"><a class="lk-ph" href="{e(q.get("source_url","#"))}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(q["image_url"])}" alt="{e(q.get("formula",""))}" onerror="this.closest('.lk').classList.add('lk-noimg');this.remove()"></a>
<div class="lk-b"><div class="lk-top"><span class="vchip {vcls}">{e(q.get("vibe",""))}</span><span class="ochip">{e(q.get("season",""))}</span><span class="ochip">{e(q.get("occasion",""))}</span><button class="lk-love" type="button" aria-pressed="false" aria-label="Love this look">♡</button></div>
<div class="lk-f">{e(q.get("formula",""))}</div><ul class="lk-p">{pcs}</ul><p class="lk-why">{e(q.get("why",""))}</p><p class="lk-you"><b>For you:</b> {e(q.get("fit_for_him",""))}</p>
<div class="lk-src"><a href="{e(q.get("source_url","#"))}" target="_blank" rel="noopener">{e(q.get("source",""))}</a> · {e(q.get("trend",""))} · <span class="lk-id">{e(q["id"])}</span></div></div></article>''')
    inspo_cards = "".join(look_card(q) for q in looks)
    inspo_nav = '<a href="#inspiration" class="navinspo">✦ Inspiration</a>' if looks else ""
    inspo_section = f'''<section id="inspiration"><h2>Inspiration</h2>
<p class="lede">Pinterest looks found from your own board (Outfits 2025): new pins in the same spirit, checked one by one. Each card says which of your pieces recreate it; most need nothing new. <b>Tap ♡ on the looks you love, then tap "Copy my picks" and send them to me.</b> I'll turn them into outfits, swapping pieces where it helps.</p>
<div class="lk-diag"><b>What lifts these looks, same style, better execution:</b> one special jacket (suede, cord, quilted or denim), two or three textures together, layers that show (a collar or tee hem under a knit), tonal or two-colour palettes, a clean boxy-top/full-leg proportion, and one sneaker colour that ties it together.</div>
<div class="lk-bar"><span class="vlabel">Show:</span><button data-ls="all" class="on">All</button><button data-ls="Spring">Spring</button><button data-ls="Summer">Summer</button><button data-ls="Autumn">Autumn</button><button data-ls="Winter">Winter</button><button data-ls="loved">♥ My picks <span id="lkcount"></span></button><button id="lkcopy" type="button" class="lk-copy">Copy my picks to send me</button><span id="lkmsg" class="muted"></span></div>
<div class="lk-grid">{inspo_cards}</div></section>''' if looks else ""

    # sizes and fit profile
    sz = json.load(open(os.path.join(HERE, "sizes.json"))) if os.path.exists(os.path.join(HERE, "sizes.json")) else []
    def sz_rows(cat):
        return "".join(f'''<tr><td>{e(r["brand"])}</td><td>{e(r["item"])}</td><td class="sz">{e(r["size"])}</td><td><span class="szst sz-{e(r["status"].lower().replace(" ","-"))}">{e(r["status"])}</span></td><td class="why">{e(r["notes"])}</td></tr>''' for r in sz if r["cat"] == cat)
    SZ_CATS = ["Trousers", "Tops & knits", "Jackets", "Shoes", "Accessories"]
    sizes_section = ('<section id="sizes"><h2>Sizes &amp; fit</h2><p class="lede">What fits you, brand by brand. Tell me how each piece fits when it arrives and I\'ll update it here, so we can predict sizes for new brands. <b>Rule:</b> between sizes, or when a brand runs small or slim, take the bigger one: you look best with room. <b>Quick guide:</b> tops M (A&amp;F knits run a little long) · knit reference: COS ladder-stitch M, about 118 cm chest and 62.5 cm long · jacket reference: Massimo Dutti blouson M, 126 cm chest, 53 cm shoulder · A&amp;F trousers and jeans 32x30 (= Massimo Dutti 40) · Studio Nicholson M with a belt · Levi\'s 32x32 (hem it) · adidas 44 = Premiata 43.</p>'
                     + "".join(f'<h3 class="cat">{e(c)}</h3><table class="sztable"><thead><tr><th>Brand</th><th>Piece</th><th>Size</th><th>Status</th><th>How it fits</th></tr></thead><tbody>{sz_rows(c)}</tbody></table>' for c in SZ_CATS if any(r["cat"] == c for r in sz))
                     + "</section>") if sz else ""

    # care: washing instructions from each piece's label (care.json)
    cr = json.load(open(os.path.join(HERE, "care.json"))) if os.path.exists(os.path.join(HERE, "care.json")) else {"items": []}
    def cr_rows(cat):
        return "".join(f'''<tr><td><span class="cbr">{e(r["brand"])}</span> {f'<a href="{e(r["url"])}" target="_blank" rel="noopener">{e(r["item"])}</a>' if r.get("url") else e(r["item"])}<div class="cfab">{e(r["fabric"])}</div></td><td>{e(r["wash"])}</td><td>{e(r["dry"])}</td><td{' class="ce"' if not r["iron"] else ''}>{e(r["iron"]) or "—"}</td><td class="why">{e(r.get("tips", ""))}</td></tr>''' for r in cr["items"] if r["cat"] == cat)
    care_section = ('<section id="care"><h2>Care</h2><p class="lede">How to wash everything you ordered, straight from each label, plus what keeps it looking new. Pieces you\'re returning aren\'t here.</p>'
                    + ('<ul class="cbasics">' + "".join(f"<li>{b}</li>" for b in cr.get("basics", [])) + "</ul>" if cr.get("basics") else "")
                    + "".join(f'<h3 class="cat">{e(c)}</h3><table class="ctable"><thead><tr><th>Piece</th><th>Wash</th><th>Dry</th><th>Iron</th><th>Tips</th></tr></thead><tbody>{cr_rows(c)}</tbody></table>' for c in SZ_CATS if any(r["cat"] == c for r in cr["items"]))
                    + "</section>") if cr["items"] else ""

    # sale watch: pieces we want, waiting for the right price (watchlist.json, updated by check_prices.py)
    wl = json.load(open(os.path.join(HERE, "watchlist.json"))) if os.path.exists(os.path.join(HERE, "watchlist.json")) else {"items": []}
    def wl_status(it):
        l = it.get("last") or {}
        b = min(p for p in (l.get("price"), l.get("member"), it["full"]) if p)
        if l.get("stock") == "out":
            return "out", f"Sold out in {it['size']}"
        if b <= it["great"]:
            return "great", "Great price: buy"
        if b <= it["target"]:
            return "target", "At target: buy"
        if l.get("price", it["full"]) < it["full"]:
            return "sale", "On sale: not yet at target"
        return "wait", "Waiting"
    def wl_row(it):
        l = it.get("last") or {}
        k, label = wl_status(it)
        now = money(l.get("price", it["full"]))
        if l.get("price", it["full"]) < it["full"]:
            now = f'<s>{money(it["full"])}</s> <b>{now}</b>'
        if l.get("member"):
            now += f'<br><span class="muted">{money(l["member"])} for members</span>'
        low = ' · <b class="lowst">low stock</b>' if l.get("stock") == "low" else ""
        hist = " → ".join(f'{money(h.get("member") or h["price"])}' for h in it.get("history", [])[-4:])
        nums = it.get("outfits", [])
        if it.get("role"):   # live numbers: outfits that use the piece, or offer it in an option box
            nums = sorted({outfit_num[o[1]] for o in OUTFITS if it["role"] in o[4] and o[1] in outfit_num}
                          | {outfit_num[on] for on, ents in PIECE_ALT.items() if on in outfit_num
                             for _, _, alts in (ents if isinstance(ents, list) else [ents]) if it["role"] in alts})
        lifts = "Lifts #" + ", #".join(str(n) for n in nums)
        return f'''<tr><td class="thumb"><a href="{e(it["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(it.get("image_url",""))}" alt="" onerror="this.remove()"></a></td>
<td><a href="{e(it["url"])}" target="_blank" rel="noopener"><b>{e(it["brand"])}</b>: {e(it["name"])}</a><div class="why">{e(it["colour"])} · size {e(it["size"])} · {lifts}. {e(it.get("why",""))}</div>{(f'<div class="wdeal"><a href="{e(it["deal"]["url"])}" target="_blank" rel="noopener">{e(it["deal"]["text"])}</a></div>') if it.get("deal") else ""}</td>
<td class="wnow">{now}{low}<div class="why">Checked {e(l.get("date",""))}{(" · " + hist) if len(it.get("history", [])) > 1 else ""}</div></td>
<td class="wtgt">{money(it["target"])}<div class="why">great: {money(it["great"])}</div></td>
<td><span class="wst w-{k}">{label}</span><div class="why">{e(it.get("when",""))}</div></td></tr>'''
    WL_TIERS = [("want", "Want now"), ("later", "Later"), ("maybe", "Specials and maybes")]
    wl_tables = "".join(f'<h3 class="cat">{t}</h3><table class="wtable"><thead><tr><th></th><th>Piece</th><th>Price now</th><th>Target</th><th>Status · best moment</th></tr></thead><tbody>{"".join(wl_row(it) for it in wl["items"] if it["tier"] == k)}</tbody></table>' for k, t in WL_TIERS if any(it["tier"] == k for it in wl["items"]))
    wl_cal = "".join(f'<li><b>{e(c["when"])}</b>: {e(c["what"])}</li>' for c in wl.get("calendar", []))
    wl_brands = "".join(f'<tr><td><b>{e(b["brand"])}</b></td><td>{e(b["signup"])}</td><td class="why">{e(b["perks"])}</td><td class="why">{e(b["sales"])}</td></tr>' for b in wl.get("brands", []))
    sale_section = ('<section id="sale-watch"><h2>Sale watch</h2><p class="lede">The pieces we really want, the price we\'re waiting for, and the best moment to buy. Prices are checked automatically on Mondays and Thursdays, and daily in sale weeks. "Great" is the price to jump at.</p>'
                    + wl_tables
                    + (f'<h3 class="cat">Sales calendar</h3><ul class="wcal">{wl_cal}</ul>' if wl_cal else "")
                    + (f'<h3 class="cat">Sign up for these</h3><p class="lede">Free memberships and newsletters that give early access or member prices. Sign up yourself, with your own email.</p><table class="wbrands"><thead><tr><th>Brand</th><th>What to join</th><th>What you get</th><th>When they have sales</th></tr></thead><tbody>{wl_brands}</tbody></table>' if wl_brands else "")
                    + "</section>") if wl["items"] else ""

    brand_section = f'''<section id="brands"><h2>Brands for you</h2><p class="lede">New brands that fit your style (relaxed, old-money, Ralph Lauren meets Copenhagen), on top of A&F, COS, Les Deux and Arket. Each has one piece picked for your shape. All ship to Portugal; EU brands have no customs.</p>{brand_html}</section>''' if brands else ""

    # shopping list
    rows = []
    top = {k for k, _ in usage.most_common(8)}
    for c in CATS:
        items = [r for r, (cat, _) in ROLE_INFO.items() if cat == c and prod.get(r, {}).get("primary") and usage[r] > 0]
        items.sort(key=lambda r: -usage[r])
        lis = []
        for r in items:
            p = prod[r]["primary"]
            star = '<span class="start">Buy first</span>' if r in top else ""
            alts = sorted_alts(prod[r])
            alt = "<br>".join(f'<a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["brand"])}: {e(a["name"])} · {money(a.get("price_eur"))}</a>' for a in alts) or '<span class="muted">-</span>'
            lis.append(f'''<tr><td class="thumb"><a href="{e(p["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(p.get("image_url",""))}" alt="" onerror="this.remove()"></a></td>
<td><div class="role">{e(ROLE_INFO[r][1])} {star}</div><a href="{e(p["url"])}" target="_blank" rel="noopener">{e(p["brand"])}: {e(p["name"])}</a> · <b>{money(p.get("price_eur"))}</b>
<div class="why">{e(p.get("fit_note",""))}</div></td><td class="altc">{alt}</td><td class="uses">{usage[r]} outfit{"s" if usage[r]!=1 else ""}</td></tr>''')
        if lis:
            rows.append(f'<h3 class="cat">{e(c)}</h3><table><thead><tr><th></th><th>Main pick</th><th>Alternatives</th><th>Used in</th></tr></thead><tbody>{"".join(lis)}</tbody></table>')

    ups = {}
    for oname, entries in PIECE_ALT.items():
        for piece, label, alts in (entries if isinstance(entries, list) else [entries]):
            if label.startswith("Upgrade"):
                for a in alts:
                    if a in ROLE_INFO and oname in outfit_num:
                        ups.setdefault(a, []).append(outfit_num[oname])
    if ups:
        lis = []
        for r, nums in ups.items():
            p = prod[r]["primary"]
            alts = sorted_alts(prod[r])
            alt = "<br>".join(f'<a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["brand"])}: {e(a["name"])} · {money(a.get("price_eur"))}</a>' for a in alts) or '<span class="muted">-</span>'
            lis.append(f'''<tr><td class="thumb"><a href="{e(p["url"])}" target="_blank" rel="noopener"><img loading="lazy" referrerpolicy="no-referrer" src="{e(p.get("image_url",""))}" alt="" onerror="this.remove()"></a></td>
<td><div class="role">{e(ROLE_INFO[r][1])}</div><a href="{e(p["url"])}" target="_blank" rel="noopener">{e(p["brand"])}: {e(p["name"])}</a> · <b>{money(p.get("price_eur"))}</b>
<div class="why">{e(p.get("fit_note",""))}</div></td><td class="altc">{alt}</td><td class="uses">Upgrades #{", #".join(str(x) for x in sorted(nums))}</td></tr>''')
        rows.append(f'<h3 class="cat">Upgrades</h3><p class="lede">Pieces you picked to lift outfits you already wear. They show as "Upgrade" boxes on those outfits.</p><table><thead><tr><th></th><th>Main pick</th><th>Alternatives</th><th>Lifts</th></tr></thead><tbody>{"".join(lis)}</tbody></table>')
    ex = [r for r in ROLE_INFO if prod.get(r, {}).get("primary") and usage[r] == 0 and r not in ups]
    if ex:
        exl = []
        for r in ex:
            p = prod[r]["primary"]; a = prod[r].get("alt")
            alt = f' · or <a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["brand"])} ({money(a.get("price_eur"))})</a>' if a else ""
            exl.append(f'<li><b>{e(ROLE_INFO[r][1])}:</b> <a href="{e(p["url"])}" target="_blank" rel="noopener">{e(p["brand"])}: {e(p["name"])}</a> · {money(p.get("price_eur"))}{alt}</li>')
        rows.append(f'<h3 class="cat">Optional extras</h3><p class="lede">You already own something that does this job, so these are only worth buying if you want a second option.</p><ul class="extras">{"".join(exl)}</ul>')
    pal = [("Ecru","#EDE6D6"),("Stone","#CBBFA8"),("Taupe","#8E7F6E"),("Grey","#BDBDB8"),("Charcoal","#3E3F41"),("Navy","#1F2A44"),("Powder blue","#A9C1DC"),("Denim","#8FA9C4"),("Brown","#5A4030")]
    palette = "".join(f'<span class="sw"><i style="background:{c}"></i>{n}</span>' for n, c in pal)
    fp = os.path.join(HERE, "favourites.json")
    saved_favs = [n for n in (json.load(open(fp)).get("saved", []) if os.path.exists(fp) else []) if any(o[1] == n for o in OUTFITS)]
    saved_favs = json.dumps(saved_favs, ensure_ascii=False).replace("</", "<\\/")
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Your Outfits</title>
<style>
:root{{--bg:#f6f4ef;--card:#fff;--text:#1f1e1c;--muted:#6f6d66;--line:#e5e1d8;--accent:#1f2a44;--chip:#efece4}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
.wrap{{max-width:1100px;margin:0 auto;padding:32px 16px 80px}}
h1{{font-size:30px;font-weight:600;letter-spacing:-.01em;margin:0 0 6px}}
.lede{{color:var(--muted);max-width:720px;margin:0 0 16px}}
.palette{{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 20px}}
.sw{{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--muted)}}
.sw i{{width:18px;height:18px;border-radius:50%;border:1px solid rgba(0,0,0,.12);display:inline-block}}
nav{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:10px 0;margin-bottom:8px;display:flex;gap:8px;flex-wrap:wrap}}
nav a{{text-decoration:none;color:var(--accent);background:var(--chip);padding:6px 12px;border-radius:999px;font-size:14px}}
h2{{font-size:24px;font-weight:600;margin:36px 0 14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;margin-bottom:18px}}
.card header{{display:flex;align-items:flex-start;gap:12px;flex-wrap:wrap}}
.num{{font-weight:700;color:var(--accent);font-size:18px;min-width:28px}}
.card h3{{margin:0;font-size:19px;font-weight:600}}
.inspo{{margin:2px 0 0;font-size:13px;color:var(--muted)}}
.tot{{margin-left:auto;font-size:13px;background:var(--chip);border-radius:999px;padding:3px 10px;white-space:nowrap}}
.note{{margin:10px 0 14px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}}
.tile{{display:flex;flex-direction:column}}
.ph{{position:relative;display:block;aspect-ratio:3/4;border-radius:10px;overflow:hidden;background:var(--chip)}}
.ph img{{width:100%;height:100%;object-fit:cover;display:block;position:relative;z-index:1;background:#fff}}
.ph span{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;padding:10px;font-size:13px;color:var(--muted)}}
.owned .ph{{background:repeating-linear-gradient(45deg,#efece4,#efece4 8px,#e8e4da 8px,#e8e4da 16px)}}
.owned .ph span{{color:#444;font-weight:600}}
.meta{{padding:8px 2px 0;font-size:13px;line-height:1.35}}
.br{{text-transform:uppercase;letter-spacing:.05em;font-size:11px;color:var(--muted)}}
.nm{{color:var(--text);text-decoration:none;display:block;margin:2px 0}}
a.nm:hover{{text-decoration:underline}}
.pr{{color:var(--muted)}}
.alt{{display:block;margin-top:3px;font-size:12px;color:var(--accent)}}
.badge{{display:inline-block;font-size:11px;background:#e1f5ee;color:#085041;border-radius:999px;padding:1px 8px;margin-bottom:4px}}
.cat{{margin:26px 0 8px;font-size:17px}}
table{{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:14px}}
th{{text-align:left;font-size:12px;color:var(--muted);font-weight:500;padding:8px 10px;border-bottom:1px solid var(--line)}}
td{{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}}
td a{{color:var(--accent)}}
.thumb{{width:64px}} .thumb img{{width:56px;height:72px;object-fit:cover;border-radius:6px;background:var(--chip)}}
.role{{font-weight:600;margin-bottom:2px}}
.why{{color:var(--muted);font-size:13px;margin-top:2px}}
.start{{font-size:11px;background:#faeeda;color:#633806;border-radius:999px;padding:1px 8px;margin-left:6px;font-weight:500}}
.uses{{white-space:nowrap;color:var(--muted)}}
.muted{{color:var(--muted)}}
.hero{{border:2px solid var(--accent)}} .herotag{{display:inline-block;background:var(--accent);color:#fff;font-size:12px;border-radius:999px;padding:2px 10px;margin-bottom:10px}}
.vchip,.ochip{{display:inline-block;font-size:11px;border-radius:999px;padding:1px 8px;margin-right:6px}}
.ochip{{background:var(--chip);color:#444441}}
.v-street{{background:#e6f1fb;color:#0c447c}} .v-mid{{background:#f1efe8;color:#444441}} .v-classy{{background:#1f2a44;color:#fff}}
.vibes{{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:0 0 6px}} .vlabel{{font-size:13px;color:var(--muted);margin-right:2px}}
.vibes button{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}}
.vibes button.on{{background:var(--accent);color:#fff;border-color:var(--accent)}}
section,article{{scroll-margin-top:64px}}
.owned-img .ph{{outline:2px solid #9fe1cb;outline-offset:-2px}}
.ph .owntag{{position:absolute;top:8px;left:8px;z-index:3;background:#0f6e56;color:#fff;font-style:normal;font-size:11px;font-weight:600;padding:3px 9px;border-radius:999px;box-shadow:0 1px 3px rgba(0,0,0,.18)}}
.tots{{margin-left:auto;display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}} .tots .tot{{margin-left:0}}
.fav{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:3px 10px;font:inherit;font-size:13px;cursor:pointer;white-space:nowrap;color:var(--muted)}} .fav.on{{background:#fff4d6;border-color:#e3c46a;color:#7a5a00;font-weight:600}} nav a.navfav{{background:#fff4d6;color:#7a5a00}} #favtools button{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 14px;font:inherit;font-size:14px;cursor:pointer}}
article.card.flash{{outline:3px solid #e3c46a;outline-offset:2px;transition:outline-color .4s}}
#rail{{position:fixed;left:0;top:72px;bottom:14px;width:34px;z-index:6;touch-action:none;user-select:none;-webkit-user-select:none;cursor:pointer}}
#rail .ticks{{position:absolute;left:0;right:0;top:0;bottom:0}}
#rail i{{position:absolute;left:7px;height:2px;width:7px;border-radius:2px;opacity:.55;transform:translateY(-1px);transition:width .12s ease,opacity .12s ease}}
#rail i.ten{{width:11px;opacity:.8}} #rail i.cur{{width:15px;opacity:1;height:3px}}
#rail b{{position:absolute;left:21px;font-size:9px;font-weight:600;line-height:1;color:var(--muted);transform:translateY(-50%);transition:opacity .12s}}
#rail .here{{position:absolute;left:24px;font-style:normal;font-size:11px;font-weight:700;color:var(--accent);background:var(--bg);padding:0 2px;border-radius:4px;transform:translateY(-50%);pointer-events:none}}
#rail.active b,#rail.active .here{{opacity:0}} #rail.active i{{opacity:.9}}
#rail .bubble{{position:absolute;left:44px;transform:translateY(-50%);background:var(--accent);color:#fff;border-radius:14px;padding:6px 14px 7px;font-size:26px;font-weight:700;line-height:1.1;white-space:nowrap;box-shadow:0 6px 18px rgba(0,0,0,.18);pointer-events:none}}
#rail .bubble small{{display:block;font-size:12px;font-weight:500;opacity:.85}}
@media (max-width:1219px){{.wrap{{padding-left:44px}}}} @media (max-width:640px){{.wrap{{padding-left:38px}} #rail{{width:30px}} #rail i{{left:5px}} #rail b{{left:18px}} #rail .here{{left:20px}}}}
.cmp{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:3px 10px;font:inherit;font-size:13px;cursor:pointer;white-space:nowrap;color:var(--muted)}}
.cmp.on{{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:600}}
nav a.navcmp{{background:#e6ebf4;color:var(--accent)}} .cmpcount:not(:empty){{margin-left:6px;background:var(--accent);color:#fff;border-radius:999px;padding:0 7px;font-size:12px}}
#cmptray{{position:fixed;left:50%;transform:translateX(-50%);bottom:max(12px,env(safe-area-inset-bottom));z-index:20;width:min(760px,calc(100vw - 24px))}}
#cmptray .ct-in{{display:flex;align-items:center;gap:8px;background:var(--accent);color:#fff;border-radius:16px;padding:8px 8px 8px 14px;box-shadow:0 10px 30px rgba(0,0,0,.25)}}
.ct-lab{{font-size:13px;font-weight:600;opacity:.85}}
#cmpchips{{display:flex;gap:6px;overflow-x:auto;flex:1;scrollbar-width:none;min-width:0}} #cmpchips::-webkit-scrollbar{{display:none}}
.cchip{{flex:0 0 auto;display:inline-flex;align-items:center;gap:4px;background:rgba(255,255,255,.14);border:0;color:#fff;border-radius:999px;padding:4px 6px 4px 10px;font:inherit;font-size:13px;cursor:pointer}}
.cchip b{{font-weight:700}} .cchip i{{font-style:normal;opacity:.7;padding:0 4px}}
.ct-go{{border:0;background:#fff;color:var(--accent);border-radius:999px;padding:8px 14px;font:inherit;font-size:14px;font-weight:700;cursor:pointer;white-space:nowrap}}
.ct-clr{{border:1px solid rgba(255,255,255,.35);background:transparent;color:#fff;border-radius:999px;padding:7px 12px;font:inherit;font-size:13px;cursor:pointer;white-space:nowrap}}
#cmptoast{{position:fixed;left:50%;transform:translateX(-50%);bottom:96px;z-index:60;font-size:13px;color:var(--text);pointer-events:none}} #cmptoast:not(:empty){{background:#fff;border:1px solid var(--line);border-radius:999px;padding:6px 14px;box-shadow:0 6px 18px rgba(0,0,0,.15);max-width:calc(100vw - 32px)}}
body.hastray .wrap{{padding-bottom:130px}} body.hastray #rail{{bottom:86px}}
body.cmpopen{{overflow:hidden}}
#cmpview{{position:fixed;inset:0;z-index:50;background:var(--bg);display:flex;flex-direction:column}}
#cmpview[hidden]{{display:none}}
.cv-bar{{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:12px 16px;border-bottom:1px solid var(--line);background:var(--bg)}}
.cv-t{{display:flex;align-items:baseline;gap:10px;flex:1;min-width:200px}} .cv-t h2{{margin:0;font-size:20px}}
.cv-btns{{display:flex;gap:6px;flex-wrap:wrap}}
.cv-btns button{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}}
.cv-close{{margin-left:auto;border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:999px;padding:6px 12px;font:inherit;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap}}
.cv-scroll{{flex:1;overflow:auto;-webkit-overflow-scrolling:touch}}
#cmpgrid{{max-width:1100px;margin:0 auto;padding:16px}} .cv-card{{margin-bottom:16px}} .cv-cardbar{{display:flex;justify-content:flex-end;align-items:center;gap:12px;margin:-4px 0 8px}} .ch-go{{font:inherit;font-size:13px;color:var(--accent);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}} .ch-x{{border:0;background:var(--chip);border-radius:999px;padding:4px 10px;cursor:pointer;font:inherit;font-size:13px}} .cv-card .tiles{{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x proximity;padding-bottom:6px;-webkit-overflow-scrolling:touch}} .cv-card .tiles > .tile{{flex:0 0 150px;scroll-snap-align:start}} mark.cv-sh{{display:block;font-style:normal;inset:auto;width:auto;height:auto;line-height:1.3;text-align:left;position:absolute;left:6px;bottom:6px;z-index:3;font-size:11px;font-weight:600;background:#fff4d6;color:#7a5a00;border-radius:999px;padding:2px 8px;box-shadow:0 1px 3px rgba(0,0,0,.12)}}
.cv-none{{max-width:520px;margin:60px auto;padding:0 16px;text-align:center;color:var(--muted)}} .cv-none b{{color:var(--text)}}
@media (max-width:640px){{
  #cmpgrid{{--lab:66px;--col:min(78vw,280px)}}
  .cv-card .tiles > .tile{{flex-basis:132px}} #cmpgrid{{padding:12px}}
  .cv-t{{min-width:0}} .cv-t h2{{font-size:17px}}
  .ct-lab{{display:none}}
  .cv-bar{{padding:10px 12px;gap:8px}} .cv-btns{{flex-wrap:nowrap;overflow-x:auto;width:100%;scrollbar-width:none}} .cv-btns::-webkit-scrollbar{{display:none}} .cv-btns button{{flex:0 0 auto}}
}}
nav a.navinspo{{background:#efe7f6;color:#5b3f86}}
.lk-diag{{background:#fff;border:1px solid var(--line);border-left:4px solid #5b3f86;border-radius:12px;padding:12px 14px;font-size:14px;margin:0 0 14px;max-width:820px}}
.lk-bar{{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:0 0 14px}}
.lk-bar button{{border:1px solid var(--line);background:#fff;border-radius:999px;padding:5px 12px;font:inherit;font-size:13px;cursor:pointer}}
.lk-bar button.on{{background:var(--accent);color:#fff;border-color:var(--accent)}} .lk-bar .lk-copy{{margin-left:auto}}
.lk-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}}
.lk{{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}}
.lk.loved{{border-color:#d46a8a;box-shadow:0 0 0 2px #f6d3de}}
.lk-ph{{display:block;aspect-ratio:2/3;background:#efede7;overflow:hidden}} .lk-ph img{{width:100%;height:100%;object-fit:contain;display:block}}
.lk.lk-noimg .lk-ph{{display:none}}
.lk-b{{padding:12px 14px;display:flex;flex-direction:column;gap:6px;flex:1}}
.lk-top{{display:flex;gap:4px;align-items:center;flex-wrap:wrap}}
.lk-love{{margin-left:auto;border:1px solid var(--line);background:#fff;border-radius:999px;width:34px;height:34px;font-size:17px;line-height:1;cursor:pointer;color:#c2456b}}
.lk-love.on{{background:#c2456b;color:#fff;border-color:#c2456b}}
.lk-f{{font-weight:700;font-size:14px;line-height:1.3}}
.lk-p{{margin:0;padding-left:18px;font-size:13px;color:var(--text)}} .lk-p li{{margin:1px 0}}
.lk-why{{margin:0;font-size:13px;color:var(--muted)}} .lk-you{{margin:0;font-size:13px}}
.lk-src{{margin-top:auto;font-size:12px;color:var(--muted)}} .lk-src a{{color:var(--muted)}} .lk-id{{font-family:ui-monospace,Menlo,monospace}}
.wst{{font-size:12px;border-radius:999px;padding:2px 8px;white-space:nowrap;background:var(--chip);display:inline-block}} .w-great,.w-target{{background:#e1f5ee;color:#085041;font-weight:700}} .w-sale{{background:#fff4d6;color:#7a5a00}} .w-out{{background:#fde8e8;color:#8a1f1f}} .lowst{{color:#8a1f1f}} .wtable td.wnow,.wtable td.wtgt{{white-space:nowrap}} .wcal{{margin:0 0 8px;padding-left:20px;line-height:1.6}} .wdeal{{margin-top:6px;font-size:13px;background:#e1f5ee;border-radius:8px;padding:6px 8px}} .wdeal a{{color:#085041}}
.sztable td.sz{{font-weight:700;white-space:nowrap}} .szst{{font-size:12px;border-radius:999px;padding:2px 8px;white-space:nowrap;background:var(--chip)}} .sz-confirmed{{background:#e1f5ee;color:#085041}} .sz-to-check{{background:#fff4d6;color:#7a5a00}} .sz-arriving,.sz-bought{{background:#e6ebf4;color:var(--accent)}} .sz-predicted,.sz-measured{{background:#efe7f6;color:#5b3f86}} .sz-too-small{{background:#fde8e8;color:#8a1f1f}}
.ctable .cbr{{font-size:12px;color:var(--muted);display:block}} .ctable .cfab{{font-size:12px;color:var(--muted);margin-top:2px}} .ctable td{{vertical-align:top}} .ctable td:first-child a{{color:var(--text);font-weight:600;text-decoration:none}} .cbasics{{margin:0 0 12px;padding-left:20px;line-height:1.6;font-size:14px}}
.ownchip{{font-size:13px;background:#e1f5ee;color:#085041;border-radius:999px;padding:3px 10px;white-space:nowrap}}
.season{{display:flex;flex-wrap:wrap;gap:6px 14px;align-items:baseline;background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:-4px 0 16px;font-size:14px}}
.season .months{{font-weight:600}} .season .temps{{color:var(--accent)}} .season .tip{{color:var(--muted);flex-basis:100%}}
.sgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px}}
.sg{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px}} .sg .ph{{aspect-ratio:4/3;background:#fff}} .sg .ph img{{object-fit:contain;background:#fff}}
.fwid{{font-size:12px;color:var(--accent);margin-top:3px}}
.wearhow{{margin-top:6px;font-size:12px;line-height:1.35;background:var(--chip);border-radius:8px;padding:6px 8px}} .wearhow span{{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:2px}} .wearhow b{{color:var(--accent);font-weight:600}}
.swapbox{{margin-top:6px;font-size:12px}} .swapbox summary{{cursor:pointer;color:var(--accent);list-style:none;line-height:1.35}} .swapbox summary::-webkit-details-marker{{display:none}}
.swapbox summary::after{{content:" ▾";}} .swapbox[open] summary::after{{content:" ▴";}} .swaplab{{font-weight:600}}
.swapgrid{{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:6px}} .swapitem{{display:block;text-decoration:none;color:var(--text);background:var(--chip);border-radius:8px;padding:5px}}
.swapph{{display:block;aspect-ratio:3/4;border-radius:6px;overflow:hidden;background:#fff;margin-bottom:4px}} .swapph img{{width:100%;height:100%;object-fit:cover;display:block}}
.swapitem b{{display:block;font-weight:600;font-size:11px;line-height:1.25}} .swapitem small{{display:block;color:var(--muted);font-size:11px;line-height:1.25}} .swapitem .trend{{display:inline-block;font-style:normal;font-size:10px;font-weight:600;background:#fff;border:1px solid var(--line);border-radius:999px;padding:1px 6px;margin:4px 0 2px}}
.swap{{display:block;margin-top:6px;font-size:13px;color:var(--muted)}} .swap a{{color:var(--accent)}}
.fitb{{display:inline-block;font-size:11px;font-weight:600;border-radius:999px;padding:2px 8px;margin-top:4px}} .fb-ok{{background:#e1f5ee;color:#085041}} .fb-mid{{background:#faeeda;color:#633806}} .fb-far{{background:#f6e3e3;color:#7a1f1f}} .fb-unk{{background:var(--chip);color:#555}}
.pgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin-bottom:8px}}
.pair{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:10px}}
.pairimgs{{display:grid;grid-template-columns:1fr 1fr;gap:8px}} .pair .ph{{aspect-ratio:1/1;background:#fff}} .pair .ph img{{object-fit:contain;background:#fff}}
.ph .lentag{{position:absolute;top:6px;left:6px;z-index:3;background:var(--accent);color:#fff;font-style:normal;font-size:11px;font-weight:600;padding:2px 8px;border-radius:999px}}
.pairhd{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:4px}} .pairhd .tot{{margin-left:auto}}
.fit{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin:0 0 18px}}
.fit h3{{margin:0 0 6px;font-size:16px}} .fit ul{{margin:0;padding-left:18px}} .fit li{{margin:4px 0}}
.extras{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 12px 12px 30px}} .extras li{{margin:4px 0}} .extras a{{color:var(--accent)}}
.foot{{margin-top:40px;color:var(--muted);font-size:13px}}
@media (max-width:640px){{nav{{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}} nav::-webkit-scrollbar{{display:none}} nav a{{flex:0 0 auto;white-space:nowrap}} .tots{{margin-left:40px;justify-content:flex-start}} .altc,.uses,th:nth-child(3),th:nth-child(4){{display:none}} .sztable thead{{display:none}} .sztable tr{{display:grid;grid-template-columns:1fr auto;grid-template-areas:"b s" "p t" "n n";gap:2px 10px;padding:10px 12px;border-bottom:1px solid var(--line)}} .sztable td{{display:block;padding:0;border:0}} .sztable td:nth-child(1){{grid-area:b;font-size:12px;color:var(--muted)}} .sztable td:nth-child(2){{grid-area:p;font-weight:600}} .sztable td:nth-child(3){{grid-area:s;text-align:right}} .sztable td:nth-child(4){{grid-area:t;text-align:right}} .sztable td:nth-child(5){{grid-area:n;margin-top:4px}} .sztable td:nth-child(5):empty{{display:none}} .ctable thead{{display:none}} .ctable tr{{display:grid;grid-template-columns:1fr 1fr;grid-template-areas:"p p" "w w" "d i" "t t";gap:4px 10px;padding:10px 12px;border-bottom:1px solid var(--line)}} .ctable td{{display:block;padding:0;border:0}} .ctable td:nth-child(1){{grid-area:p}} .ctable td:nth-child(2){{grid-area:w}} .ctable td:nth-child(3){{grid-area:d}} .ctable td:nth-child(4){{grid-area:i}} .ctable td:nth-child(5){{grid-area:t;margin-top:2px}} .ctable td:nth-child(5):empty{{display:none}} .ctable td.ce{{display:none}} .ctable td:nth-child(2)::before{{content:"Wash: ";font-weight:600}} .ctable td:nth-child(3)::before{{content:"Dry: ";font-weight:600}} .ctable td:nth-child(4)::before{{content:"Iron: ";font-weight:600}} .wtable thead,.wbrands thead{{display:none}} .wtable tr{{display:grid;grid-template-columns:64px 1fr auto;grid-template-areas:"i p p" "i n t" "s s s";gap:4px 10px;padding:10px 12px;border-bottom:1px solid var(--line)}} .wtable td{{display:block;padding:0;border:0}} .wtable td:nth-child(1){{grid-area:i}} .wtable td:nth-child(2){{grid-area:p}} .wtable td:nth-child(3){{grid-area:n}} .wtable td:nth-child(4){{grid-area:t;text-align:right}} .wtable td:nth-child(5){{grid-area:s}} .wbrands tr{{display:block;padding:10px 12px;border-bottom:1px solid var(--line)}} .wbrands td{{display:block;padding:2px 0;border:0}}}}
</style></head><body><div class="wrap">
<h1>Your outfits for every season</h1>
<p class="lede"><b>Your style: relaxed, clean casual with an old-money touch, like Ralph Lauren meets Copenhagen.</b> Your Pinterest board sets the direction, not a copy of it. Knits, shirts, sweatshirts, hoodies and tees, with jeans or wide trousers, Sambas and Gazelles, a puffer or vest. It ranges from street to classy, so there's always something for the occasion. {n} outfits mixing new pieces with clothes you already own. Click any piece to open the shop page.</p>
<p class="lede"><b>Accessories:</b> 2–3 per outfit, with one statement spot: the neck or the wrists, not both loaded. Necklaces only where the neckline shows, sunglasses by day, and the Rolex for dinners and the classier looks. Each outfit already lists the right amount.</p>
<div class="palette">{palette}</div>
<div class="fit"><h3>What suits you, based on your photos</h3><ul>
<li><b>Cropped, boxy tops with wide trousers is your best shape.</b> You're tall with long legs, so you carry wide trousers easily, and tops that end at the hip balance them. Your best photos show this (brown puffer, check jacket), and you've noticed it yourself. The pieces on this page lean cropped and boxy for that reason. Avoid tops that cover the zip of your trousers.</li>
<li><b>Rise matters with cropped tops.</b> Go for mid or high-rise trousers so no skin shows when you lift your arms. Tuck long knits loosely at the front or fold them under at the hem.</li>
<li><b>Navy, brown and blue beat black on you.</b> With dark hair and light skin, navy and dark brown give contrast without looking harsh. Your black puffer is the weakest piece in your photos, and the brown one does the same job better.</li>
<li><b>Blue is your colour.</b> It's in five of your eight photos (linen shirt, stripes, suede sneakers, denim) and it always works.</li>
<li><b>Hem length:</b> wide trousers should touch the shoe with a small fold, not swallow it. A few of your jeans pile up too much at the bottom. A tailor can take them up for about €10.</li>
<li><b>Accessories:</b> silver jewellery gives an outfit character without being loud. Try a silver chain bracelet or cuff on the wrist opposite your watch, and a thin chain or small pendant at the neck. Most outfits here use one or two pieces.</li>
<li><b>Graphics:</b> one fun graphic piece per outfit (Guinness knit, rugby polo, stripes) keeps it personal. Pair it with plain, darker trousers so it looks intentional.</li>
</ul></div>
<div class="vibes"><span class="vlabel">Show:</span><button data-f="all" class="on">All</button><button data-f="v-street">Street</button><button data-f="v-mid">In between</button><button data-f="v-classy">Classy</button><button data-f="ready">Ready to wear</button><button data-f="one">One piece away</button></div>
<nav><a href="#favourites" class="navfav">★ Favourites</a><a href="#compare" class="navcmp">⇄ Compare<span class="cmpcount"></span></a><a href="#spring">Spring</a><a href="#summer">Summer</a><a href="#autumn">Autumn</a><a href="#winter">Winter</a><a href="#special">Special occasions</a>{inspo_nav}<a href="#caps">Caps</a><a href="#brands">Brands</a><a href="#shopping-list">Shopping list</a><a href="#sizes">Sizes &amp; fit</a>{'<a href="#care">Care</a>' if care_section else ''}<a href="#sale-watch">Sale watch</a></nav>
<section id="favourites"><h2>Favourites <span id="favcount" class="muted"></span></h2>
<p class="lede" id="favempty">Tap <b>☆ Favourite</b> on any outfit and it shows up here. Taps are only kept in this browser, and browsers can clear them (Safari does after about a week without a visit). To keep them for good, on every device, tap <b>Copy the list to send me</b> and paste it to me: I'll save them into the page.</p>
<div id="favlist"></div><p id="favtools" hidden><button id="favcmp" type="button">⇄ Compare these</button> <button id="favcopy" type="button">Copy the list to send me</button> <span id="favmsg" class="muted"></span></p></section>
{"".join(sec)}
{inspo_section}
{sg_section if SHOW_SUNGLASSES else ''}
{nk_section if SHOW_NECKLACES else ''}
{cap_section}
{brand_section}
<section id="shopping-list"><h2>Shopping list</h2>
<p class="lede">Every piece once, with a main pick and up to two alternatives (often a cheaper one and an independent-label one). Pieces marked "Buy first" appear in the most outfits, so start with those. Outfit totals use the main picks.</p>
{"".join(rows)}</section>
{sizes_section}
{care_section}
{sale_section}
<p class="foot">Prices and stock were checked on 6 October 2026 and can change. Sizing and fit vary by brand, so check each shop's size guide. Tiles marked "You have this" are things you already own. A green outline means a photo of your piece (or the closest match); striped tiles are pieces without a photo yet.</p>
</div>
<div id="cmptray" hidden><div class="ct-in"><span class="ct-lab">Compare</span><div id="cmpchips"></div><button id="cmpgo" type="button" class="ct-go">Compare</button><button id="cmpclr" type="button" class="ct-clr">Clear all</button></div></div>
<div id="cmptoast" role="status" aria-live="polite"></div>
<div id="cmpview" hidden role="dialog" aria-modal="true" aria-labelledby="cmptitle"><div class="cv-bar"><div class="cv-t"><h2 id="cmptitle">Compare outfits</h2><span id="cmpsub" class="muted"></span><button id="cvclose" type="button" class="cv-close" aria-label="Close compare">✕ Close</button></div><div class="cv-btns"><button id="cvfav" type="button">＋ Add favourites</button><button id="cvlink" type="button">Copy link</button><button id="cvclr" type="button">Clear all</button></div></div><div class="cv-scroll" id="cvscroll"><div id="cmpgrid"></div></div></div>
<div id="rail" role="navigation" aria-label="Outfit index"><div class="ticks"></div><em class="here"></em><div class="bubble" hidden></div></div>
<script>
document.querySelectorAll('.vibes button').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelectorAll('.vibes button').forEach(x=>x.classList.toggle('on',x===b));
  const f=b.dataset.f;
  document.querySelectorAll('article.card').forEach(c=>{{c.style.display=(f==='all'||c.dataset.vibe===f||(f==='ready'&&c.dataset.ready==='yes')||(f==='one'&&c.dataset.ready==='one'))?'':'none';}});
}}));
(function(){{
  const KEY='wardrobe-favs', OFF='wardrobe-favs-off', SAVED={saved_favs};
  let local=[], off=[];
  try{{local=JSON.parse(localStorage.getItem(KEY)||'[]')||[];}}catch(e){{local=[];}}
  try{{off=JSON.parse(localStorage.getItem(OFF)||'[]')||[];}}catch(e){{off=[];}}
  let favs=[];
  const merge=()=>{{favs=[...new Set(local.concat(SAVED.filter(n=>!off.includes(n))))];}};
  const save=()=>{{try{{localStorage.setItem(KEY,JSON.stringify(local));localStorage.setItem(OFF,JSON.stringify(off));}}catch(e){{}}}};
  merge(); window.getFavs=()=>favs.slice();
  const list=document.getElementById('favlist');
  const originals=[...document.querySelectorAll('section:not(#favourites) article.card')];
  function render(){{
    list.innerHTML='';
    const picked=originals.filter(c=>favs.includes(c.dataset.name));
    picked.forEach(c=>{{const k=c.cloneNode(true);k.removeAttribute('id');k.querySelectorAll('[id]').forEach(x=>x.removeAttribute('id'));list.appendChild(k);}});
    document.getElementById('favempty').hidden=picked.length>0;
    document.getElementById('favtools').hidden=picked.length===0;
    document.getElementById('favcount').textContent=picked.length?'('+picked.length+')':'';
    document.querySelectorAll('article.card').forEach(c=>{{
      const on=favs.includes(c.dataset.name), b=c.querySelector('.fav');
      if(b){{b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);b.textContent=on?'★ Favourite':'☆ Favourite';}}
    }});
  }}
  document.addEventListener('click',ev=>{{
    const b=ev.target.closest('.fav'); if(!b) return;
    const n=b.closest('article.card').dataset.name;
    if(favs.includes(n)){{local=local.filter(x=>x!==n); if(SAVED.includes(n)&&!off.includes(n)) off.push(n);}}
    else{{local=local.concat([n]); off=off.filter(x=>x!==n);}}
    merge(); save(); render();
  }});
  document.getElementById('favcopy').addEventListener('click',()=>{{
    const txt='My favourite outfits: '+originals.filter(c=>favs.includes(c.dataset.name)).map(c=>'#'+parseInt(c.querySelector('.num').textContent,10)+' '+c.dataset.name).join(', ');
    const msg=document.getElementById('favmsg');
    const done=()=>{{msg.textContent='Copied.';}};
    try{{navigator.clipboard.writeText(txt).then(done,()=>{{msg.textContent=txt;}});}}catch(e){{msg.textContent=txt;}}
  }});
  render();
}})();
(function(){{
  const sec=document.getElementById('inspiration'); if(!sec) return;
  const KEY='wardrobe-inspo'; let loved=[];
  try{{loved=JSON.parse(localStorage.getItem(KEY)||'[]')||[];}}catch(e){{loved=[];}}
  const save=()=>{{try{{localStorage.setItem(KEY,JSON.stringify(loved));}}catch(e){{}}}};
  const cards=[...sec.querySelectorAll('.lk')]; let filt='all';
  function sync(){{
    cards.forEach(c=>{{const on=loved.includes(c.dataset.id);c.classList.toggle('loved',on);const b=c.querySelector('.lk-love');b.classList.toggle('on',on);b.textContent=on?'♥':'♡';b.setAttribute('aria-pressed',on);
      c.style.display=(filt==='all'||(filt==='loved'?on:c.dataset.season===filt))?'':'none';}});
    document.getElementById('lkcount').textContent=loved.length?'('+loved.length+')':'';
  }}
  sec.addEventListener('click',e=>{{
    const l=e.target.closest('.lk-love'); if(l){{const id=l.closest('.lk').dataset.id; loved=loved.includes(id)?loved.filter(x=>x!==id):loved.concat([id]); save(); sync(); return;}}
    const f=e.target.closest('[data-ls]'); if(f){{filt=f.dataset.ls; sec.querySelectorAll('[data-ls]').forEach(b=>b.classList.toggle('on',b===f)); sync();}}
  }});
  document.getElementById('lkcopy').addEventListener('click',()=>{{
    const msg=document.getElementById('lkmsg');
    if(!loved.length){{msg.textContent='Tap ♡ on a few looks first.';return;}}
    const txt='My inspiration picks: '+cards.filter(c=>loved.includes(c.dataset.id)).map(c=>c.dataset.id+' ('+c.querySelector('.lk-f').textContent+')').join('; ');
    try{{navigator.clipboard.writeText(txt).then(()=>{{msg.textContent='Copied.';}},()=>{{msg.textContent=txt;}});}}catch(e){{msg.textContent=txt;}}
  }});
  sync();
}})();

(function(){{
  const KEY='wardrobe-compare', MAX=8;
  const CATS=[["Outerwear","Outerwear"],["Knitwear & tops","Tops & knits"],["Trousers","Trousers"],["Shoes","Shoes"],["Accessories","Accessories"]];
  const cards=[...document.querySelectorAll('section:not(#favourites) article.card')];
  const byName=new Map(cards.map(c=>[c.dataset.name,c]));
  const num=c=>parseInt(c.querySelector('.num').textContent,10);
  const $=id=>document.getElementById(id);
  const tray=$('cmptray'), chips=$('cmpchips'), view=$('cmpview'), grid=$('cmpgrid'), toast=$('cmptoast');
  let sel=[];
  try{{sel=JSON.parse(localStorage.getItem(KEY)||'[]')||[];}}catch(e){{sel=[];}}
  sel=sel.filter(n=>byName.has(n));
  const save=()=>{{try{{localStorage.setItem(KEY,JSON.stringify(sel));}}catch(e){{}}}};
  const ordered=()=>sel.map(n=>byName.get(n)).filter(Boolean).sort((a,b)=>num(a)-num(b));
  const esc=t=>String(t).replace(/[&<>"]/g,ch=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[ch]));
  let toastT=0; function say(m){{toast.textContent=m;clearTimeout(toastT);toastT=setTimeout(()=>toast.textContent='',2200);}}

  function sync(){{
    const list=ordered();
    document.querySelectorAll('article.card').forEach(c=>{{
      const b=c.querySelector('.cmp'); if(!b) return;
      const on=sel.includes(c.dataset.name);
      b.classList.toggle('on',on); b.setAttribute('aria-pressed',on); b.textContent=on?'✓ Comparing':'＋ Compare';
    }});
    chips.innerHTML=list.map(c=>'<button class="cchip" type="button" data-rm="'+esc(c.dataset.name)+'" title="Remove '+esc(c.dataset.name)+'"><b>'+num(c)+'</b> '+esc(c.dataset.name)+'<i aria-hidden="true">✕</i></button>').join('');
    $('cmpgo').textContent='Compare ('+list.length+')';
    tray.hidden=list.length===0 || !view.hidden;
    document.body.classList.toggle('hastray',!tray.hidden);
    document.querySelectorAll('.cmpcount').forEach(x=>x.textContent=list.length||'');
  }}
  function toggle(name){{
    if(sel.includes(name)) sel=sel.filter(n=>n!==name);
    else if(sel.length>=MAX){{say('Up to '+MAX+' outfits at a time. Remove one first.');return;}}
    else sel=sel.concat([name]);
    save(); sync(); if(!view.hidden) render();
  }}
  function clearAll(){{sel=[];save();sync();if(!view.hidden)render();}}
  function addFavs(){{
    let favs=window.getFavs?window.getFavs():[];
    favs=favs.filter(n=>byName.has(n)&&!sel.includes(n));
    if(!favs.length){{say('No favourites to add yet: tap ☆ Favourite on an outfit.');return;}}
    const room=MAX-sel.length; sel=sel.concat(favs.slice(0,room)); save(); sync(); if(!view.hidden) render();
    if(favs.length>room) say('Added '+room+'. The limit is '+MAX+' at a time.');
  }}

  function render(){{
    const list=ordered();
    $('cmpsub').textContent=list.length?list.length+' outfit'+(list.length>1?'s':'')+(list.length>1?' · shared pieces marked in gold':' · add one more to compare'):'';
    const sc=$('cvscroll'), none=sc.querySelector('.cv-none');
    if(!list.length){{
      grid.innerHTML='';
      if(!none) sc.insertAdjacentHTML('beforeend','<div class="cv-none"><p><b>Nothing to compare yet.</b></p><p>Tap <b>＋ Compare</b> on any outfit card, or use <b>＋ Add favourites</b> above to add your favourites in one go.</p></div>');
      return;
    }}
    if(none) none.remove();
    const where={{}};
    list.forEach(c=>c.querySelectorAll('.tiles > .tile').forEach(t=>{{(where[t.dataset.key]=where[t.dataset.key]||[]).push(num(c));}}));
    grid.innerHTML='';
    list.forEach(c=>{{
      const n=num(c), k=c.cloneNode(true);
      k.removeAttribute('id'); k.querySelectorAll('[id]').forEach(x=>x.removeAttribute('id'));
      k.classList.remove('flash'); k.classList.add('cv-card'); k.style.display=''; k.querySelectorAll('img[loading="lazy"]').forEach(i=>i.loading='eager');
      const bar=document.createElement('div'); bar.className='cv-cardbar';
      bar.innerHTML='<button class="ch-go" type="button" data-go="'+n+'">Go to outfit</button><button class="ch-x" type="button" data-rm="'+esc(c.dataset.name)+'">✕ Remove</button>';
      k.insertBefore(bar,k.firstChild);
      k.querySelectorAll('.tiles > .tile').forEach(t=>{{
        const others=(where[t.dataset.key]||[]).filter(x=>x!==n);
        if(others.length){{const b=document.createElement('mark');b.className='cv-sh';b.textContent='Also in #'+others.join(', #');(t.querySelector('.ph')||t).appendChild(b);}}
      }});
      grid.appendChild(k);
    }});
  }}
  let lastFocus=null;
  function open(push){{
    lastFocus=document.activeElement; render(); view.hidden=false; document.body.classList.add('cmpopen'); sync();
    if(push!==false){{try{{history.pushState({{cmp:1}},'',location.pathname+location.search+'#compare='+ordered().map(num).join(','));}}catch(e){{}}}}
    $('cvclose').focus();
  }}
  function close(fromPop){{
    if(view.hidden) return;
    view.hidden=true; document.body.classList.remove('cmpopen'); sync();
    if(!fromPop){{try{{if(history.state&&history.state.cmp) history.back(); else history.replaceState(null,'',location.pathname+location.search);}}catch(e){{}}}}
    if(lastFocus&&lastFocus.focus) lastFocus.focus();
  }}
  window.addEventListener('popstate',()=>{{if(!view.hidden) close(true);}});
  document.addEventListener('keydown',e=>{{if(e.key==='Escape'&&!view.hidden) close();}});

  document.addEventListener('click',e=>{{
    const b=e.target.closest('.cmp'); if(b){{toggle(b.closest('article.card').dataset.name);return;}}
    const rm=e.target.closest('[data-rm]'); if(rm){{toggle(rm.dataset.rm);return;}}
    const nav=e.target.closest('a.navcmp'); if(nav){{e.preventDefault(); open(); return;}}
    const go=e.target.closest('[data-go]');
    if(go){{
      const t=document.getElementById('o'+go.dataset.go); close();
      setTimeout(()=>{{ if(t.style.display==='none'){{const all=document.querySelector('.vibes button[data-f="all"]');if(all)all.click();}}
        const nv=document.querySelector('nav'); const place=()=>window.scrollTo(0,t.getBoundingClientRect().top+window.scrollY-nv.offsetHeight-8);
        place(); setTimeout(place,250); t.classList.add('flash'); setTimeout(()=>t.classList.remove('flash'),1600);}},60);
    }}
  }});
  $('cmpgo').addEventListener('click',()=>open());
  $('cmpclr').addEventListener('click',clearAll);
  $('cvclr').addEventListener('click',clearAll);
  $('cvfav').addEventListener('click',addFavs);
  $('cvclose').addEventListener('click',()=>close());
  $('favcmp').addEventListener('click',()=>{{
    let favs=window.getFavs?window.getFavs():[];
    favs=favs.filter(n=>byName.has(n)); if(!favs.length) return;
    sel=favs.slice(0,MAX); save(); sync(); open(); if(favs.length>MAX) say('Showing the first '+MAX+' favourites.');
  }});
  $('cvlink').addEventListener('click',()=>{{
    const url=location.origin+location.pathname+'#compare='+ordered().map(num).join(',');
    const done=()=>{{const b=$('cvlink');b.textContent='Link copied';setTimeout(()=>b.textContent='Copy link',1600);}};
    try{{navigator.clipboard.writeText(url).then(done,()=>prompt('Copy this link:',url));}}catch(e){{prompt('Copy this link:',url);}}
  }});
  const m=location.hash.match(/^#compare=([0-9,]+)/);
  if(m){{const nums=m[1].split(',').map(Number);const names=cards.filter(c=>nums.includes(num(c))).map(c=>c.dataset.name).slice(0,MAX);if(names.length){{sel=names;save();}}}}
  window.addEventListener('hashchange',()=>{{
    const h=location.hash.match(/^#compare=([0-9,]+)/); if(!h||!view.hidden) return;
    const nums=h[1].split(',').map(Number); const names=cards.filter(c=>nums.includes(num(c))).map(c=>c.dataset.name).slice(0,MAX);
    if(names.length){{sel=names;save();sync();open(false);}}
  }});
  sync();
  if(m&&sel.length){{try{{history.replaceState(null,'',location.pathname+location.search);history.pushState({{cmp:1}},'',location.pathname+location.search+'#compare='+ordered().map(num).join(','));}}catch(e){{}} open(false);}}
}})();
(function(){{
  const COL={{spring:'#6f9a5b',summer:'#c99a2e',autumn:'#b0602f',winter:'#56739a',special:'#8a63b3'}};
  const rail=document.getElementById('rail'), ticks=rail.querySelector('.ticks'), bub=rail.querySelector('.bubble'), here=rail.querySelector('.here'), nav=document.querySelector('nav');
  const cards=[...document.querySelectorAll('section:not(#favourites) article.card')], N=cards.length, els=[], labels=[];
  const num=c=>parseInt(c.querySelector('.num').textContent,10);
  cards.forEach((c,i)=>{{
    const t=document.createElement('i'), top=((i+.5)/N*100)+'%', n=num(c);
    t.style.top=top; t.style.background=COL[c.closest('section').id]||'#999';
    if(n%10===0){{t.className='ten';const b=document.createElement('b');b.textContent=n;b.style.top=top;ticks.appendChild(b);labels.push([i,b]);}}
    ticks.appendChild(t); els.push(t);
  }});
  const fit=()=>{{rail.style.top=(nav.offsetHeight+12)+'px';}};
  const idxAt=y=>{{const r=ticks.getBoundingClientRect();return Math.max(0,Math.min(N-1,Math.floor((y-r.top)/r.height*N)));}};
  function jump(i){{
    const t=cards[i];
    if(t.style.display==='none'){{const all=document.querySelector('.vibes button[data-f="all"]');if(all)all.click();}}
    const place=()=>window.scrollTo(0,t.getBoundingClientRect().top+window.scrollY-nav.offsetHeight-8);
    place();setTimeout(place,250);
  }}
  function show(i){{
    const c=cards[i], sec=c.closest('section').querySelector('h2').textContent;
    bub.innerHTML=num(c)+'<small></small>'; bub.querySelector('small').textContent=c.dataset.name+' · '+sec;
    bub.style.top=els[i].style.top; bub.hidden=false; rail.classList.add('active');
    els.forEach((t,j)=>{{const d=Math.abs(j-i);t.style.width=d<5?(7+(5-d)*4)+'px':'';}});
  }}
  function hide(){{bub.hidden=true;rail.classList.remove('active');els.forEach(t=>t.style.width='');}}
  let drag=false,last=-1,hideT=0;
  rail.addEventListener('pointerdown',e=>{{e.preventDefault();clearTimeout(hideT);drag=true;try{{rail.setPointerCapture(e.pointerId);}}catch(_){{}}const i=idxAt(e.clientY);show(i);if(i!==last){{jump(i);last=i;}}}});
  rail.addEventListener('pointermove',e=>{{const i=idxAt(e.clientY);if(drag){{show(i);if(i!==last){{jump(i);last=i;}}}}else if(e.pointerType==='mouse'){{show(i);}}}});
  const end=()=>{{if(!drag)return;drag=false;if(last>=0){{const t=cards[last];t.classList.add('flash');setTimeout(()=>t.classList.remove('flash'),1500);}}last=-1;hideT=setTimeout(hide,700);}};
  rail.addEventListener('pointerup',end); rail.addEventListener('pointercancel',end);
  rail.addEventListener('pointerleave',()=>{{if(!drag)hide();}});
  let raf=0;
  function current(){{
    raf=0; const y=nav.getBoundingClientRect().bottom+60; let k=-1;
    for(let i=0;i<N;i++){{const r=cards[i].getBoundingClientRect();if(!r.height)continue;if(r.top<=y)k=i;else break;}}
    const past=k===N-1&&cards[k].getBoundingClientRect().bottom<y;
    els.forEach((t,j)=>t.classList.toggle('cur',j===k&&!past));
    if(k>=0&&!past){{here.textContent=num(cards[k]);here.style.top=els[k].style.top;here.hidden=false;labels.forEach(([j,b])=>b.style.opacity=Math.abs(j-k)<3?0:'');}}
    else{{here.hidden=true;labels.forEach(([,b])=>b.style.opacity='');}}
  }}
  window.addEventListener('scroll',()=>{{if(!raf)raf=requestAnimationFrame(current);}},{{passive:true}});
  window.addEventListener('resize',()=>{{fit();current();}});
  fit(); current();
}})();
</script></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(doc)
    missing = [r for r in ROLE_INFO if r not in prod]
    print("outfits:", n, "| roles with products:", len(prod), "| missing:", missing)

if __name__ == "__main__":
    build()
