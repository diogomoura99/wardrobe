import json, html, sys, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outfits-autumn-winter-2026.html")
e = html.escape

CATS = ["Outerwear", "Knitwear & tops", "Trousers", "Shoes", "Accessories"]
ROLE_INFO = {
    "vest_puffer": ("Outerwear", "Puffer vest"),
    "jacket_varsity": ("Outerwear", "Varsity jacket"),
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
    "cardigan_mohair": ("Knitwear & tops", "Grey mohair cardigan"),
    "shoe_mexico66": ("Shoes", "Cream & brown Onitsuka Mexico 66"),
    "knit_check": ("Knitwear & tops", "Cream checkerboard knit"),
    "shirt_terry": ("Knitwear & tops", "Navy terry shirt"),
    "jewelry_ring": ("Accessories", "Silver ring"),
}
ALIAS = {}
BLOCK_BRANDS_SHOES = ("Axel Arigato", "Filling Pieces")
NO_CAPS = False
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
    "own_stripe_knit": ("Knitwear & tops", "Your green & cream striped knit"),
    "own_blue_linen": ("Knitwear & tops", "Your light-blue linen shirt"),
    "own_navy_linen": ("Knitwear & tops", "Your navy linen shirt"),
    "own_guinness": ("Knitwear & tops", "Your Guinness knit"),
    "own_rugby": ("Knitwear & tops", "Your Cowboys rugby polo"),
    "own_stripe_ls": ("Knitwear & tops", "Your blue striped long-sleeve"),
    "own_brown_tee": ("Knitwear & tops", "Your brown tee"),
    "own_cos_blue": ("Knitwear & tops", "Your COS blue merino jumper"),
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
   ["own_cos_cream", "own_midwash", "own_samba_maroon", "own_cap_navy", "own_watch"]),
  ("Autumn", "Brown jacket", "Your board: brown jacket open over a knit",
   "Your brown barn jacket open over the Guinness knit, light jeans and burgundy Sambas. Made entirely from clothes you own.",
   ["own_brown_jacket_af", "own_guinness", "own_lightwash", "own_samba_maroon", "own_cap_navy", "own_cuban_bracelet"]),
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
   "Your sage textured jacket over the blue stripes, khaki jeans and green Spezials. Greens and blues that work together.",
   ["own_sage_jacket", "own_stripe_ls", "own_beige_jeans", "own_samba_green", "own_cuban_bracelet", "own_sunnies_jaconelli"]),
  ("Autumn", "Guinness, upgraded", "Your Guinness knit, one step up",
   "Keep the fun knit, with navy wide trousers and your burgundy Sambas so it looks deliberate.",
   ["own_guinness", "own_cos_navy_trouser", "own_samba_maroon", "own_cuban_bracelet"]),

  ("Winter", "Brown puffer", "Your brown puffer + striped knit",
   "Your brown Ultra puffer over the navy and green striped knit, cream jeans and white sneakers.",
   ["own_brown_puffer", "own_stripe_navy_green", "own_af_cream", "own_spezial_cream", "own_watch", "own_cap_navy"]),
  ("Winter", "Puffer vest", "Your board: puffer vests over knits",
   "Vest over your blue cable knit with light jeans and your navy Spezials. Warm without bulk, very Copenhagen.",
   ["vest_puffer", "own_blue_cable", "own_lightwash", "own_spezial_navy", "own_cap_navy", "own_watch"]),
  ("Winter", "Varsity", "Your board: navy varsity + white jeans + NY cap",
   "Varsity jacket, white tee, cream jeans and white sneakers. Preppy street.",
   ["jacket_varsity", "own_af_white_tee", "own_af_cream", "own_spezial_cream", "own_cap_navy", "own_ix_figaro"]),
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
   ["sweat_grey", "own_af_cream", "own_spezial_navy", "own_cap_navy", "own_watch"]),
  ("Winter", "Black puffer, done right", "Your black puffer, with better colours",
   "Black looks harsh with beige. With grey and white it looks clean and intentional.",
   ["own_black_puffer", "own_ymc_grey", "own_af_cream", "own_spezial_cream", "own_sd_pendant", "own_watch"]),
  ("Winter", "Rainy day", "Built for Portuguese winters",
   "Your COS waxed jacket over a chocolate knit with your neutral grey Levi's. A true grey with no blue cast sits cleanly with the browns and khaki. Burgundy leather Sambas and the Western cap handle the rain better than suede, and the burgundy warms up the browns.",
   ["own_cos_waxed", "own_howlin_brown", "own_levis_grey", "own_cuban_bracelet", "own_cap_western", "own_samba_maroon"]),
  ("Winter", "Cold street", "Your board: hoodies + puffers",
   "Brown puffer over a blue hoodie with khaki jeans and your navy Spezials, which pick up the blue of the hoodie.",
   ["own_brown_puffer", "hoodie_graphic_blue", "own_beige_jeans", "own_spezial_navy", "own_cap_navy", "own_cuban_bracelet"]),
  ("Winter", "Coffee run", "Your photo: blue knit + check scarf",
   "Let the white tee show at the hem. Your navy, white and light-blue check scarf is the statement, and it picks up the blue knit and light jeans.",
   ["own_cos_blue", "own_af_white_tee", "own_lightwash", "own_ld_scarf", "own_sunnies_jaconelli", "own_spezial_cream"]),

  ("Summer", "Club tee", "Your board: graphic tees + clogs + cap",
   "Boxy graphic tee, white jeans, suede clogs and a cap. Easy warm-day look.",
   ["own_hotel_tee", "own_af_cream", "clog_suede", "own_cap_navy", "own_cuban_bracelet"]),
  ("Spring", "Knit polo & white jeans", "Your board: polo + white jeans",
   "Knit polo with white jeans and your navy suede Spezials. Brown, cream and navy: the classiest spring look here.",
   ["knit_polo", "own_af_cream", "own_spezial_navy", "own_sunnies_jaconelli", "bracelet_cuff"]),
  ("Spring", "Blue knit & graphic", "Your board: blue knit + graphic tee flat lay",
   "Blue knit over a graphic tee, light jeans and your white Premiatas.",
   ["own_cos_blue", "own_hotel_tee", "own_lightwash", "own_white_sneakers", "own_sd_pendant", "own_cuban_bracelet"]),
  ("Spring", "Weekend hoodie", "Your rust hoodie",
   "Rust hoodie, dark grey baggy jeans, white Premiatas and the navy cap. All yours.",
   ["own_rust_hoodie", "own_af_greywash", "own_white_sneakers", "own_cap_navy", "own_watch"]),
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
   ["own_hotel_tee", "own_pinstripe", "clog_suede", "own_cap_navy", "own_ix_figaro", "own_sd_pendant"]),
  ("Spring", "Rugby & navy", "Your Cowboys rugby polo, one step up",
   "Your Cowboys rugby polo with navy wide trousers. More contrast than the all-white version.",
   ["own_rugby", "own_cos_navy_trouser", "own_white_sneakers", "own_sunnies_jaconelli", "own_cuban_bracelet"]),
  ("Spring", "Sunday lunch", "Built from your style",
   "Chocolate knit, navy wide trousers and your light-blue Spezials. Brown, navy and light blue is a classic mix.",
   ["own_howlin_brown", "own_cos_navy_trouser", "own_gazelle", "own_ix_figaro", "own_watch"]),
  ("Autumn", "Blue & brown", "Your new COS jumper + your new brown trousers",
   "Light blue and dark brown is one of the best combinations for your colouring. Brown suede Premiatas tie it together.",
   ["own_cos_blue", "own_af_brown", "own_premiata", "own_cuban_bracelet", "own_watch"]),
  ("Autumn", "Check & navy", "Your check jacket, with navy",
   "Check jacket open over a navy knit, cream jeans and burgundy Sambas. The navy picks up the check.",
   ["own_check_jacket", "own_arket_navy", "own_af_cream", "own_samba_maroon", "own_watch", "own_sd_pendant"]),
  ("Autumn", "Brown & burgundy", "Your board formula, in brown",
   "Chocolate knit, light jeans, burgundy Sambas, your cream and brown Western cap and your Serge DeNimes pendant over the knit. Warm and easy.",
   ["own_howlin_brown", "own_lightwash", "own_samba_maroon", "own_cap_western", "own_sd_pendant"]),
  ("Winter", "Tonal brown", "Your brown puffer, head to toe",
   "Your brown AirCloud puffer, cream jumper, dark brown trousers and brown suede Premiatas. Warm, tonal and classy.",
   ["own_aircloud_brown", "own_cos_cream", "own_af_brown", "own_premiata", "own_watch", "own_sd_pendant"]),
  ("Winter", "Black puffer & burgundy", "Your black puffer with a colour pop",
   "Black puffer over your light-grey Oasis sweatshirt with mid-blue jeans. Black and light grey is a clean contrast, and the burgundy Sambas are the colour pop. No navy next to the black.",
   ["own_black_puffer", "own_oasis", "own_midwash", "own_samba_maroon", "own_watch", "own_cuban_bracelet"]),
  ("Spring", "Blue & cream", "Your COS blue jumper, spring version",
   "Light blue jumper with cream jeans and your navy Sporty & Rich Spezials. Exactly the Sporty & Rich look, and all the clothes are yours.",
   ["own_cos_blue", "own_af_cream", "own_spezial_navy", "own_sunnies_asos", "own_watch"]),
  ("Spring", "Cowboys & khaki", "Your rugby polo with khaki jeans",
   "Your Cowboys rugby polo with khaki jeans, navy Spezials and the navy cap. Collegiate preppy, the same idea as the Sporty & Rich collab.",
   ["own_rugby", "own_beige_jeans", "own_spezial_navy", "own_cap_navy", "own_cuban_bracelet"]),
  ("Summer", "Riviera tee", "Summer, softer and more casual",
   "Your cream tee with white linen trousers, light-blue Spezials, your clear lilac sunglasses and the IX figaro chain and bracelet. Pastel and relaxed.",
   ["own_af_tee_cream", "own_white_linen", "own_gazelle", "own_sunnies_asos", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Summer", "Camp collar", "Your lace camp-collar shirt",
   "Your lace camp-collar shirt worn open, cream jeans and suede clogs.",
   ["own_lace_camp", "own_af_cream", "clog_suede", "own_sunnies_jaconelli", "own_ix_figaro", "own_sd_pendant"]),
  ("Summer", "Blue linen & olive", "Your light-blue linen shirt",
   "Your light-blue linen shirt, top two buttons open over your white tank, your olive pleated baggy trousers, white Premiatas and the navy cap. Blue and olive is a fresh summer pairing.",
   ["own_blue_linen", "own_af_tank_white", "own_af_olive_pleated", "own_white_sneakers", "own_cap_navy", "own_ix_figaro"]),
  ("Summer", "Graphic & light denim", "Your board: graphic tees",
   "Your Hotel tee with light-wash baggy jeans, navy Spezials and the cap, plus the layered necklaces. Summer street, no shorts.",
   ["own_hotel_tee", "own_lightwash", "own_spezial_navy", "own_cap_navy", "own_ix_figaro", "own_sd_pendant"]),
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
   ["own_coastal", "own_cos_navy_trouser", "own_samba_maroon", "own_cap_navy", "own_watch"]),
  ("Autumn", "Oasis day", "Your Oasis sweatshirt, as you wore it",
   "Oasis sweatshirt with your dark grey baggy jeans, burgundy Sambas and the cap. Street, but considered.",
   ["own_oasis", "own_af_greywash", "own_samba_maroon", "own_cap_navy", "own_sd_pendant"]),
  ("Autumn", "Blue cable & grey", "Your blue cable knit",
   "Blue cable knit, dark grey jeans, white sneakers and the navy cap.",
   ["own_blue_cable", "own_af_greywash", "own_spezial_cream", "own_cap_navy", "own_cuban_bracelet"]),
  ("Winter", "Cord jacket & stripes", "Your cream cord jacket, winter",
   "Cream cord jacket over the navy and green striped knit, mid-blue jeans and brown Premiatas.",
   ["own_cream_cord_jacket", "own_stripe_navy_green", "own_midwash", "own_premiata", "own_watch", "own_cap_navy"]),
  ("Spring", "Harrington & white", "Your Polo harrington, lighter",
   "Navy harrington over a white tee with cream jeans and white sneakers. Clean and classic.",
   ["own_polo_harrington", "own_af_white_tee", "own_af_cream", "own_spezial_cream", "own_sunnies_jaconelli", "own_watch"]),
  ("Spring", "Sage & brown", "Your sage jacket + brown trousers",
   "Sage textured jacket over your cream tee, dark brown trousers and white Premiatas. Cream sits more softly between sage and brown than white.",
   ["own_sage_jacket", "own_af_tee_cream", "own_af_brown", "own_white_sneakers", "own_sd_pendant", "own_sunnies_jaconelli"]),
  ("Spring", "Navy zip & khaki", "Your navy zip knit, smarter",
   "Navy zip knit half-open over your light-blue linen shirt, collar out, with khaki jeans, brown suede Premiatas and the Rolex. Navy, light blue and khaki: classic.",
   ["own_navy_zip_knit", "own_blue_linen", "own_beige_jeans", "own_premiata", "own_watch"]),
  ("Summer", "Seersucker whites", "Your adidas seersucker shirt",
   "Cream seersucker shirt with your white linen trousers, brown suede Premiatas, the IX chain and the Rolex.",
   ["own_seersucker_camp", "own_white_linen", "own_premiata", "own_watch", "own_ix_figaro"]),
  ("Summer", "Sage stripes", "Your sage striped linen shirt",
   "Sage striped linen shirt, top two buttons open over your white tank, ash pleated trousers, white Premiatas and your clear lilac sunglasses. Soft pastels together.",
   ["own_ms_sage_stripe", "own_af_tank_white", "own_af_ash_pleated", "own_white_sneakers", "own_sunnies_asos", "own_cuban_bracelet"]),
  ("Summer", "Blue stripes & denim", "Your blue striped linen shirt",
   "Blue striped linen shirt, top two buttons open over your white tank, light-wash baggy jeans, burgundy Sambas and the cap.",
   ["own_ms_blue_stripe", "own_af_tank_white", "own_lightwash", "own_samba_maroon", "own_cap_navy", "own_sd_pendant"]),
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
   ["own_af_white_tee", "own_af_olive_pleated", "own_spezial_navy", "own_cap_navy", "own_ix_figaro", "own_ix_figaro_bracelet"]),
  ("Summer", "Brown tee & cream", "Warm summer neutrals",
   "Your brown tee with cream jeans, light-blue Spezials, your Western cap and the Cuban bracelet. Warm, with one cool accent at the feet.",
   ["own_brown_tee", "own_af_cream", "own_gazelle", "own_cap_western", "own_cuban_bracelet"]),
  ("Summer", "Grey tee & navy", "Summer evening, casual",
   "Your grey tee with the COS navy wide-leg trousers, white Premiatas and the layered necklaces. Simple and cool-toned for a warm evening.",
   ["own_af_tee_grey", "own_cos_navy_trouser", "own_white_sneakers", "own_ix_figaro", "own_sd_pendant"]),
  ("Summer", "Hotel tee & khaki", "Your board: graphic tees",
   "Your Hotel tee with khaki jeans, green Spezials and the navy cap. Ivory, khaki and a green accent.",
   ["own_hotel_tee", "own_beige_jeans", "own_samba_green", "own_cap_navy", "own_cuban_bracelet"]),
  ("Summer", "Cream tee & light denim", "The easiest summer outfit",
   "Your cream tee with light-wash baggy jeans, white Premiatas, the navy cap and your clear lilac sunglasses.",
   ["own_af_tee_cream", "own_lightwash", "own_white_sneakers", "own_cap_navy", "own_sunnies_asos"]),
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
  ("Summer", "Navy & cream tank", "A cream tank under navy linen",
   "Navy linen shirt, top two buttons open over a cream ribbed tank, cream baggy jeans, burgundy Sambas and your Western cap. Navy, cream and burgundy: preppy and warm.",
   ["own_navy_linen", "tank_cream", "own_af_cream", "own_samba_maroon", "own_cap_western", "own_cuban_bracelet"]),
  ("Summer", "Blue & brown Riviera", "A brown tank under light-blue linen",
   "Light-blue linen shirt, top two buttons open over a chocolate ribbed tank, white linen trousers, brown suede Premiatas, the IX chain and the Rolex. Light blue and brown, your best pairing, made summery.",
   ["own_blue_linen", "tank_brown", "own_white_linen", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Summer", "Stripes & navy tank", "A navy tank under blue stripes",
   "Blue striped linen shirt, top two buttons open over a navy ribbed tank, ash pleated trousers, white Premiatas and the Rolex. Blue, navy and stone: easy old money for lunch.",
   ["own_ms_blue_stripe", "tank_navy", "own_af_ash_pleated", "own_white_sneakers", "own_watch", "own_cuban_bracelet"]),
  ("Autumn", "Navy & taupe cord", "Your new Levi's taupe cord",
   "Your Arket navy jumper with the taupe Levi's cord, burgundy Sambas and the navy cap. Navy and taupe are softer than navy and khaki, and the burgundy gives it a lift.",
   ["own_arket_navy", "own_levis_taupe", "own_samba_maroon", "own_cap_navy", "own_cuban_bracelet"]),
  ("Autumn", "Brown & grey", "Your new grey Levi's",
   "Your brown barn jacket over the cream ladder-stitch knit, neutral grey Levi's and brown suede Premiatas. Brown, cream and a true grey: very Copenhagen.",
   ["own_brown_jacket_af", "own_cos_cream", "own_levis_grey", "own_premiata", "own_watch", "own_sd_pendant"]),
  ("Winter", "Taupe & light blue", "Your Levi's taupe cord, winter",
   "Dark brown puffer over your light-blue COS jumper, taupe Levi's cord, off-white Spezials and your navy check scarf. The scarf ties the light blue to the warm browns.",
   ["own_brown_puffer", "own_cos_blue", "own_levis_taupe", "own_spezial_cream", "own_ld_scarf", "own_watch"]),
  ("Winter", "Tonal grey", "Your grey Levi's, winter",
   "Brown AirCloud puffer over your grey YMC knit with the grey Levi's, burgundy Sambas and the Western cap. Grey on grey, warmed up by the brown and burgundy.",
   ["own_aircloud_brown", "own_ymc_grey", "own_levis_grey", "own_samba_maroon", "own_cap_western", "own_cuban_bracelet"]),
  ("Autumn", "Waxed & mohair", "The COS waxed jacket, styled the COS way",
   "Your COS waxed jacket over a grey brushed-mohair cardigan and your white tee, ash pleated baggies and brown suede Premiatas. Waxed cotton, cord and mohair in quiet browns and greys: how COS styles it, minus the loafers.",
   ["own_cos_waxed", "cardigan_mohair", "own_af_white_tee", "own_af_ash_pleated", "own_premiata", "own_watch", "own_ix_figaro"]),
  ("Winter", "Waxed & cream cord", "The COS waxed jacket, winter",
   "Your COS waxed jacket over your cream ladder-stitch knit, taupe Levi's cord and burgundy Sambas. The chocolate cord collar picks up the cord trousers, and the leather Sambas cope with rain.",
   ["own_cos_waxed", "own_cos_cream", "own_levis_taupe", "own_samba_maroon", "own_watch", "own_sd_pendant"]),
  ("Special Summer", "Navy terry Riviera", "New piece: navy cable-terry shirt",
   "Navy cable-terry shirt with the top buttons open, your light beige linen baggy trousers, brown suede Premiatas, the IX chain and the Rolex. The Riviera in the evening.",
   ["shirt_terry", "own_af_linen_baggy", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Special Winter", "Chocolate coat", "New piece: chocolate wool coat",
   "Chocolate wool coat over your Arket navy jumper, ash pleated trousers, white Premiatas and your navy check scarf. Brown, navy and stone: the classiest winter look here.",
   ["coat_wool", "own_arket_navy", "own_af_ash_pleated", "own_white_sneakers", "own_ld_scarf", "own_watch"]),
  ("Special Summer", "Embroidered linen night", "Special piece: A&F embroidered linen shirt",
   "Your warm-beige A&F linen shirt with tonal embroidered medallions, top two buttons open, your COS navy pleated wide-leg trousers, brown suede Premiatas, the IX chain and the Rolex. A deep, neutral navy under the beige gives the contrast the olive lacked.",
   ["own_af_embroidered", "own_cos_navy_trouser", "own_premiata", "own_ix_figaro", "own_watch"]),
  ("Special Winter", "Checkerboard knit", "Special piece: Les Deux check knit",
   "Les Deux's cream checkerboard wool knit with mid-blue baggy jeans, brown suede Premiatas and your brown AirCloud puffer worn open. A modern knit that keeps your cream-and-brown palette.",
   ["own_aircloud_brown", "knit_check", "own_midwash", "own_premiata", "own_watch"]),
]

# backup inner layer per outfit, for when the main one is in the wash (first is the best swap)
INNER_ALT = {
  "Striped half-zip": ["own_af_tee_grey", "own_hotel_tee"],
  "Zip cardigan": ["own_af_white_tee", "own_hotel_tee"],
  "Overshirt layers": ["own_af_white_tee", "own_hotel_tee"],
  "Check jacket": ["own_af_white_tee", "own_af_tee_cream"],
  "Stripes & sage jacket": ["own_af_white_tee", "own_af_tee_cream"],
  "Varsity": ["own_hotel_tee", "own_af_tee_cream"],
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
  "Riviera tee": ["own_af_white_tee", "own_af_tee_grey"],
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
  "Waxed & mohair": ["own_af_tee_cream", "own_af_tee_grey"],
}

# other pieces worth showing under a specific tile: (piece, label, [options])
PIECE_ALT = {
  "Striped half-zip": ("own_polo_halfzip", "Also great here", ["knit_halfzip"]),
  "Date night": ("own_polo_halfzip", "Also great here", ["knit_halfzip"]),
  "Camp collar": ("own_af_cream", "Lighter for hot days", ["own_af_linen_baggy"]),
  "Brown linen day": [("own_af_cream", "Lighter for hot days", ["own_af_linen_baggy"]),
                      ("own_af_tank_white", "Even better here", ["tank_cream"])],
  "Brown tee & cream": ("own_af_cream", "Lighter for hot days", ["own_af_linen_baggy"]),
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
  "Blue & cream": ("own_spezial_navy", "Timeless option", ["shoe_premiata"]),
  "Harrington & white": ("own_spezial_cream", "Other shoes to try", ["shoe_premiata_cream", "shoe_mexico66", "shoe_gg_navy"]),
  "Black knit & cream": ("own_spezial_cream", "Other shoes to try", ["shoe_premiata_cream", "shoe_premiata_black", "shoe_gg_black"]),
}

# how to wear the necklaces in each outfit: (where, detail), shown under the chain / pendant tile
NECKLACES = ("own_ix_figaro", "own_sd_pendant")
NECK_WEAR = {
  "Blue knit & graphic": ("Outside", "over the blue knit, so the pendant sits on the wool. The graphic tee stays underneath."),
  "Sunday lunch": ("Outside", "over the chocolate knit, just below the crew neck. Silver shows up well on dark brown."),
  "Sage & brown": ("Outside the tee, inside the jacket", "on the cream tee, framed by the open sage jacket."),
  "Pinstripe & graphic": ("Outside", "both over the tee."),
  "Riviera tee": ("Outside", "over the cream tee, at the collarbone."),
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
  "Waxed & mohair": ("Outside the tee, inside the cardigan", "on the white tee, in the V of the mohair cardigan."),
  "Varsity": ("Outside the tee, inside the jacket", "on the white tee, framed by the open varsity jacket."),
  "Tonal brown": ("Outside the knit, inside the puffer", "over the cream jumper. Wear the puffer open so it shows."),
  "Waxed & cream cord": ("Outside the knit, inside the jacket", "over the cream knit. Wear the jacket open so it shows."),
  "Seersucker whites": ("On skin, inside the shirt", "in the open collar of the seersucker shirt."),
}

# other jackets to try on in the mirror (owned first; same colour family and warmth)
OUTER_ALT = {
  "AirCloud & cable": ["own_brown_puffer", "own_cos_waxed"],
  "Tonal brown": ["own_brown_puffer", "own_brown_jacket_af"],
  "Brown puffer": ["own_aircloud_brown", "own_cos_waxed"],
  "Cold street": ["own_aircloud_brown", "own_cos_waxed"],
  "Black puffer, done right": ["own_brown_puffer", "own_aircloud_brown"],
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
  "Waxed & mohair": ["own_brown_jacket_af"],
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
  "Seersucker whites": ("Classy", "Holiday dinner"),
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
  "Waxed & mohair": ("Classy", "Lunch / city"),
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
            return f'''<div class="tile owned-img"><a class="ph" href="{e(info["url"])}" target="_blank" rel="noopener">
<em class="owntag">✓ You have it</em><img loading="lazy" referrerpolicy="no-referrer" src="{e(info["image_url"])}" alt="{e(label)}" onerror="this.parentElement.classList.add('noimg');this.remove()"><span>{e(label)}</span></a>
<div class="meta"><div class="br">{e(info.get("brand",""))}</div><div class="nm">{e(label)}</div>{note}{swap}</div></div>'''
        return f'''<div class="tile owned"><div class="ph"><em class="owntag">✓ You have it</em><span>{e(label)}</span></div>
<div class="meta"><div class="nm">{e(label)}</div></div></div>'''
    p = prod.get(key, {}).get("primary")
    cat, label = ROLE_INFO[key]
    if not p:
        return ""
    alts = sorted_alts(prod[key])
    alt_html = "".join(f'<a class="alt" href="{e(a["url"])}" target="_blank" rel="noopener">or {e(a["brand"])} · {money(a.get("price_eur"))}</a>' for a in alts)
    return f'''<div class="tile"><a class="ph" href="{e(p["url"])}" target="_blank" rel="noopener">
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
            out[outer] = swap_box("Other jacket to try", OUTER_ALT[name], prod)
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
        OUTFITS = [(a, b, c, d, [k for k in pcs if k != "own_cap_navy"]) for a, b, c, d, pcs in OUTFITS]
    prod = load_products()
    usage = Counter(k for *_, pieces in OUTFITS for k in pieces if k in ROLE_INFO and prod.get(k, {}).get("primary"))
    seasons = ["Spring", "Summer", "Autumn", "Winter", "Special occasions"]
    sid = {s: s.lower().replace(" ", "-") for s in seasons}
    sid["Special occasions"] = "special"
    order = ["Spring", "Summer", "Autumn", "Winter"]
    special = sorted([o for o in OUTFITS if o[0].startswith("Special ")], key=lambda o: order.index(o[0].split(" ", 1)[1]))
    sec = []
    n = 0
    for s in seasons:
        cards = []
        for season, name, inspo, note, pieces in (special if s == "Special occasions" else OUTFITS):
            if s != "Special occasions" and season != s:
                continue
            n += 1
            sw = swaps_for(name, pieces, prod)
            tiles = "".join(tile(k, prod, sw.get(k, "")) for k in sorted(pieces, key=lambda k: CATS.index((ROLE_INFO.get(k) or OWNED.get(k))[0])))
            total = sum(float(prod[k]["primary"].get("price_eur") or 0) for k in pieces if k in ROLE_INFO and prod.get(k, {}).get("primary"))
            hero = False
            n_own = sum(1 for k in pieces if k in OWNED)
            n_all = sum(1 for k in pieces if k in OWNED or prod.get(k, {}).get("primary"))
            vibe, occ = VIBE.get(name, ("In between", "Everyday"))
            vcls = {"Street": "v-street", "In between": "v-mid", "Classy": "v-classy"}[vibe]
            cards.append(f'''<article class="card{' hero' if hero else ''}" data-name="{e(name)}" data-vibe="{vcls}" data-ready="{'yes' if n_all and n_own == n_all else ('one' if n_all - n_own == 1 else 'no')}">{'<div class="herotag">Your reference look</div>' if hero else ''}<header><span class="num">{n:02d}</span><div><h3>{e(name)}</h3>
<p class="inspo"><span class="vchip {vcls}">{e(vibe)}</span>{('<span class="ochip">' + e(season.split(" ", 1)[1]) + '</span>') if season.startswith("Special ") else ""}<span class="ochip">{e(occ)}</span>{e(inspo)}</p></div><span class="tots"><button class="fav" type="button" aria-pressed="false" aria-label="Save to favourites">☆ Favourite</button><span class="ownchip">You own {n_own} of {n_all}</span><span class="tot">{("New pieces: " + money(total)) if total else "All pieces you own"}</span></span></header>
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
<div class="fwid">{e(q.get("construction",""))}</div>{'<div class="fitb fb-ok">✓ Shape very close to yours</div>' if q.get("similarity")=="high" else ('<div class="fitb fb-mid">Shallower than yours</div>' if q.get("similarity")=="medium" else '')}<div class="why">{e(q.get("fit_note",""))}</div></div></div>''')
    CAP_GROUPS = [("green", "Washed green: the one colour worth adding", "For your green adidas, the Eagles sweater and sage pieces."),
                  ("navy", "Navy: only if your '47 Base Runner doesn't fit", "Your navy cap already covers 16 outfits."),
                  ("brown", "Chocolate brown (optional)", "Your Western cap already covers the brown outfits."),
                  ("stone", "Stone and cream (optional)", "Would overlap with your cream/brown Western."),
                  ("burgundy", "Burgundy (just for variety)", "Navy already does this job.")]
    cap_cards = "".join(f'<h3 class="cat">{e(t)} <span class="muted" style="font-weight:400;font-size:14px">— {e(d)}</span></h3><div class="sgrid">' + "".join(cap_card(q) for q in caps if q.get("colour_group") == g) + '</div>' for g, t, d in CAP_GROUPS if any(q.get("colour_group") == g for q in caps))

    cap_section = f'''<section id="caps"><h2>Caps</h2><p class="lede">What suits you, going by your A&F Western snapback (which looks nothing like A&F's current snapbacks): <b>a pre-curved brim and a rounded crown that holds its shape</b>, classy rather than a flat-brim, boxy "classic snapback". Soft dad hats that collapse flat on your thick hair don't work either. <b>You're covered with your two caps:</b> navy for the cool and denim outfits (and with burgundy Sambas), cream/brown for the warm ones. Try your navy '47 Base Runner first; it's the same relaxed, curved type as your Western. All caps below are matched to your Western cap's shape.</p>{cap_cards}</section>''' if caps else ""

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

    ex = [r for r in ROLE_INFO if prod.get(r, {}).get("primary") and usage[r] == 0]
    if ex:
        exl = []
        for r in ex:
            p = prod[r]["primary"]; a = prod[r].get("alt")
            alt = f' · or <a href="{e(a["url"])}" target="_blank" rel="noopener">{e(a["brand"])} ({money(a.get("price_eur"))})</a>' if a else ""
            exl.append(f'<li><b>{e(ROLE_INFO[r][1])}:</b> <a href="{e(p["url"])}" target="_blank" rel="noopener">{e(p["brand"])}: {e(p["name"])}</a> · {money(p.get("price_eur"))}{alt}</li>')
        rows.append(f'<h3 class="cat">Optional extras</h3><p class="lede">You already own something that does this job, so these are only worth buying if you want a second option.</p><ul class="extras">{"".join(exl)}</ul>')
    pal = [("Ecru","#EDE6D6"),("Stone","#CBBFA8"),("Taupe","#8E7F6E"),("Grey","#BDBDB8"),("Charcoal","#3E3F41"),("Navy","#1F2A44"),("Powder blue","#A9C1DC"),("Denim","#8FA9C4"),("Brown","#5A4030")]
    palette = "".join(f'<span class="sw"><i style="background:{c}"></i>{n}</span>' for n, c in pal)
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
@media (max-width:640px){{.tots{{margin-left:40px;justify-content:flex-start}} .altc,.uses,th:nth-child(3),th:nth-child(4){{display:none}}}}
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
<nav><a href="#favourites" class="navfav">★ Favourites</a><a href="#spring">Spring</a><a href="#summer">Summer</a><a href="#autumn">Autumn</a><a href="#winter">Winter</a><a href="#special">Special occasions</a><a href="#sunglasses">Sunglasses</a><a href="#necklaces">Necklaces</a><a href="#caps">Caps</a><a href="#brands">Brands</a><a href="#shopping-list">Shopping list</a></nav>
<section id="favourites"><h2>Favourites <span id="favcount" class="muted"></span></h2>
<p class="lede" id="favempty">Tap <b>☆ Favourite</b> on any outfit and it shows up here. Favourites are saved on this phone or browser.</p>
<div id="favlist"></div><p id="favtools" hidden><button id="favcopy" type="button">Copy the list to send me</button> <span id="favmsg" class="muted"></span></p></section>
{"".join(sec)}
{sg_section}
{nk_section}
{cap_section}
{brand_section}
<section id="shopping-list"><h2>Shopping list</h2>
<p class="lede">Every piece once, with a main pick and up to two alternatives (often a cheaper one and an independent-label one). Pieces marked "Buy first" appear in the most outfits, so start with those. Outfit totals use the main picks.</p>
{"".join(rows)}</section>
<p class="foot">Prices and stock were checked on 6 October 2026 and can change. Sizing and fit vary by brand, so check each shop's size guide. Tiles marked "You have this" are things you already own. A green outline means a photo of your piece (or the closest match); striped tiles are pieces without a photo yet.</p>
</div>
<script>
document.querySelectorAll('.vibes button').forEach(b=>b.addEventListener('click',()=>{{
  document.querySelectorAll('.vibes button').forEach(x=>x.classList.toggle('on',x===b));
  const f=b.dataset.f;
  document.querySelectorAll('article.card').forEach(c=>{{c.style.display=(f==='all'||c.dataset.vibe===f||(f==='ready'&&c.dataset.ready==='yes')||(f==='one'&&c.dataset.ready==='one'))?'':'none';}});
}}));
(function(){{
  const KEY='wardrobe-favs';
  let favs=[];
  try{{favs=JSON.parse(localStorage.getItem(KEY)||'[]')||[];}}catch(e){{favs=[];}}
  const save=()=>{{try{{localStorage.setItem(KEY,JSON.stringify(favs));}}catch(e){{}}}};
  const list=document.getElementById('favlist');
  const originals=[...document.querySelectorAll('section:not(#favourites) article.card')];
  function render(){{
    list.innerHTML='';
    const picked=originals.filter(c=>favs.includes(c.dataset.name));
    picked.forEach(c=>{{const k=c.cloneNode(true);k.querySelectorAll('[id]').forEach(x=>x.removeAttribute('id'));list.appendChild(k);}});
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
    favs=favs.includes(n)?favs.filter(x=>x!==n):favs.concat([n]);
    save(); render();
  }});
  document.getElementById('favcopy').addEventListener('click',()=>{{
    const txt='My favourite outfits: '+originals.filter(c=>favs.includes(c.dataset.name)).map(c=>'#'+parseInt(c.querySelector('.num').textContent,10)+' '+c.dataset.name).join(', ');
    const msg=document.getElementById('favmsg');
    const done=()=>{{msg.textContent='Copied.';}};
    try{{navigator.clipboard.writeText(txt).then(done,()=>{{msg.textContent=txt;}});}}catch(e){{msg.textContent=txt;}}
  }});
  render();
}})();
</script></body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(doc)
    missing = [r for r in ROLE_INFO if r not in prod]
    print("outfits:", n, "| roles with products:", len(prod), "| missing:", missing)

if __name__ == "__main__":
    build()
