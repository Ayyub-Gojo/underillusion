"""Branche AdMob dans les projets Android et iOS à partir de ads.json."""
import json, os, re, plistlib
cfg = json.load(open("ads.json", encoding="utf-8"))
TEST = "3940256099942544"
# Blocs de test officiels de Google
TEST_UNITS = {
    "android": {"banner": "ca-app-pub-3940256099942544/9214589741", "interstitial": "ca-app-pub-3940256099942544/1033173712"},
    "ios": {"banner": "ca-app-pub-3940256099942544/2435281174", "interstitial": "ca-app-pub-3940256099942544/4411468910"},
}
out = {"interstitialEvery": int(cfg.get("interstitialEvery", 2)), "testing": {}}
for pf in ("android", "ios"):
    c = cfg.get(pf) or {}
    for k in ("appId", "banner", "interstitial"):
        if not re.fullmatch(r"ca-app-pub-\d{16}[~/]\d{10}", c.get(k, "")):
            raise SystemExit(f"ads.json : identifiant {pf}.{k} invalide : {c.get(k)!r}")
    if cfg.get("useTestAds", False):
        out[pf] = dict(TEST_UNITS[pf])
        out["testing"][pf] = True
        print(f"⚠️  {pf} : useTestAds = true, pubs de démo (pas de revenus)")
    else:
        out[pf] = {"banner": c["banner"], "interstitial": c["interstitial"]}
        out["testing"][pf] = TEST in json.dumps(c)
        print(f"{pf} : " + ("identifiants de TEST (pas de revenus)" if out["testing"][pf] else "VRAIES pubs"))

with open("www/ads-config.js", "w", encoding="utf-8") as f:
    f.write("window.UI_ADS=" + json.dumps(out) + ";\n")

man = "android/app/src/main/AndroidManifest.xml"
if os.path.exists(man):
    s = open(man, encoding="utf-8").read()
    if "com.google.android.gms.ads.APPLICATION_ID" not in s:
        s = re.sub(r"(<application\b[^>]*>)", r'\1\n        <meta-data android:name="com.google.android.gms.ads.APPLICATION_ID" android:value="@string/admob_app_id"/>', s, count=1)
        open(man, "w", encoding="utf-8").write(s)
    st = "android/app/src/main/res/values/strings.xml"
    x = open(st, encoding="utf-8").read()
    x = re.sub(r'\s*<string name="admob_app_id">[^<]*</string>', "", x)
    x = x.replace("</resources>", f'    <string name="admob_app_id">{cfg["android"]["appId"]}</string>\n</resources>')
    open(st, "w", encoding="utf-8").write(x)
    print("AdMob Android OK")

pl = "ios/App/App/Info.plist"
if os.path.exists(pl):
    d = plistlib.load(open(pl, "rb"))
    d["GADApplicationIdentifier"] = cfg["ios"]["appId"]
    d["GADIsAdManagerApp"] = True
    d["SKAdNetworkItems"] = [{"SKAdNetworkIdentifier": "cstr6suwn9.skadnetwork"}]
    d["NSUserTrackingUsageDescription"] = "Cet identifiant sert à afficher des publicités plus pertinentes. Le jeu reste gratuit grâce à elles."
    plistlib.dump(d, open(pl, "wb"))
    print("AdMob iOS OK")
