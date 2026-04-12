#!/bin/bash
# IndexNow — notifie Bing de toutes les pages du site
# Usage : bash indexnow-ping.sh
# A lancer depuis Git Bash après chaque git push

KEY="A8A911547D7C17BDDBE856B293F83A46"
HOST="cv-robin.duale.fr"

curl -s -X POST "https://www.bing.com/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"host\": \"${HOST}\",
    \"key\": \"${KEY}\",
    \"keyLocation\": \"https://${HOST}/${KEY}.txt\",
    \"urlList\": [
      \"https://${HOST}/\",
      \"https://${HOST}/fr/\",
      \"https://${HOST}/en/\",
      \"https://${HOST}/fr/a-propos.html\",
      \"https://${HOST}/fr/parcours.html\",
      \"https://${HOST}/fr/temoignages.html\",
      \"https://${HOST}/fr/contact.html\",
      \"https://${HOST}/fr/perspectives/\",
      \"https://${HOST}/fr/perspectives/je-suis-le-produit.html\",
      \"https://${HOST}/fr/perspectives/ia-accelerateur-organisationnel.html\",
      \"https://${HOST}/en/about.html\",
      \"https://${HOST}/en/track-record.html\",
      \"https://${HOST}/en/references.html\",
      \"https://${HOST}/en/contact.html\",
      \"https://${HOST}/en/perspectives/\",
      \"https://${HOST}/en/perspectives/i-am-the-product.html\",
      \"https://${HOST}/en/perspectives/ai-organizational-accelerator.html\"
    ]
  }" \
  -w "\nStatut HTTP : %{http_code}\n"

echo "Ping IndexNow envoyé à Bing pour ${HOST}"
