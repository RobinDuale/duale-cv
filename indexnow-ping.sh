#!/bin/bash
# IndexNow — notifie Bing et Yandex de toutes les pages du site
# Usage : bash indexnow-ping.sh
# A lancer depuis Git Bash après chaque git push

KEY="A8A911547D7C17BDDBE856B293F83A46"
HOST="cv-robin.duale.fr"

PAYLOAD="{
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
      \"https://${HOST}/fr/perspectives/avantage-competitif-humain.html\",
      \"https://${HOST}/en/about.html\",
      \"https://${HOST}/en/track-record.html\",
      \"https://${HOST}/en/references.html\",
      \"https://${HOST}/en/contact.html\",
      \"https://${HOST}/en/perspectives/\",
      \"https://${HOST}/en/perspectives/i-am-the-product.html\",
      \"https://${HOST}/en/perspectives/ai-organizational-accelerator.html\",
      \"https://${HOST}/en/perspectives/competitive-edge-is-human.html\",
      \"https://${HOST}/fr/faq.html\",
      \"https://${HOST}/en/faq.html\",
      \"https://${HOST}/fr/mentions-legales.html\",
      \"https://${HOST}/en/legal-notice.html\"
    ]
  }"

echo "--- Ping Bing ---"
curl -s -X POST "https://www.bing.com/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${PAYLOAD}" \
  -w "Statut HTTP Bing : %{http_code}\n"

echo "--- Ping Yandex ---"
curl -s -X POST "https://yandex.com/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "${PAYLOAD}" \
  -w "Statut HTTP Yandex : %{http_code}\n"

echo ""
echo "IndexNow envoyé à Bing + Yandex pour ${HOST}"
