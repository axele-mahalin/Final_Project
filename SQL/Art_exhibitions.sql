#Query 1: Number of museums by region in France

SELECT region, COUNT(nom_du_musee) AS "nombre de musées"
FROM visitors
GROUP BY region
ORDER BY 2 DESC;

#Query 2: Number of exhibitions in Paris and breakdown by Type of price

SELECT type_de_prix, COUNT(Titre) AS "nombre d'expositions"
FROM Paris_exhibitions
GROUP BY type_de_prix
ORDER BY 2 DESC;

#Query 3: Top 10 Parisian museums in terms of exhibitions available

SELECT nom_du_lieu, COUNT(exhibitions.Titre) AS "nombre d'expositions"
FROM exhibitions.Paris_exhibitions AS exhibitions
LEFT JOIN exhibitions.visitors AS visitors
	ON exhibitions.nom_du_lieu = visitors.nom_du_musee
GROUP BY nom_du_lieu
ORDER BY 2 DESC
LIMIT 10;

#Query 4: Top 10 Parisian museums in terms of visitors and % of paid versus free

SELECT nom_du_musee, SUM(TOTAL) AS "nombre de visiteurs", ROUND(SUM(payant) / SUM(total) * 100) AS "% payant", ROUND(SUM(gratuit) / SUM(total) * 100) AS "% gratuit"
FROM visitors
GROUP BY nom_du_musee
ORDER BY 2 DESC
LIMIT 10;

#Query 5: Top 10 Parisian museums in terms of exhibitions average duration

SELECT nom_officiel_du_musée, ROUND(AVG(exhibitions.durée)) AS "durée moyenne (en jours)"
FROM exhibitions.museums AS museums
LEFT JOIN exhibitions.Paris_exhibitions AS exhibitions
	ON museums.nom_officiel_du_musée = exhibitions.nom_du_lieu
GROUP BY nom_officiel_du_musée
ORDER BY 2 DESC
LIMIT 10;


