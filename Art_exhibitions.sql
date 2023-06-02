#Query 1: Number of museums by region in France

SELECT REGION, COUNT(`NOM DU MUSEE`) AS "NOMBRE DE MUSEES"
FROM visitors
GROUP BY REGION
ORDER BY 2 DESC;

#Query 2: Number of exhibitions in Paris and breakdown by Type of price

SELECT `Type de prix`, COUNT(Titre) AS "Nombre d'expositions"
FROM Paris_exhibitions
GROUP BY `Type de prix`
ORDER BY 2 DESC;

#Query 3: Top 10 Parisian museums in terms of exhibitions available

SELECT `Nom du lieu`, COUNT(exhibitions.Titre) AS "Nombre d'expositions"
FROM exhibitions.Paris_exhibitions AS exhibitions
LEFT JOIN exhibitions.visitors AS visitors
	ON exhibitions.`Nom du lieu` = visitors.`NOM DU MUSEE`
GROUP BY `Nom du lieu`
ORDER BY 2 DESC
LIMIT 10;

#Query 4: Number of visitors by audience

/*
SELECT exhibitions.audience, SUM(visitors.TOTAL) AS "Total", SUM(visitors.PAYANT) AS "Payant", SUM(visitors.GRATUIT) AS "Gratuit"
FROM exhibitions.Paris_exhibitions AS exhibitions
INNER JOIN exhibitions.visitors AS visitors
	ON exhibitions.`Nom du lieu` = visitors.`NOM DU MUSEE`
GROUP BY exhibitions.audience
ORDER BY 2 DESC;
*/

#OR Query 4: Top 10 Parisian museums in terms of visitors and % of paid versus free

SELECT `NOM DU MUSEE`, SUM(TOTAL) AS "NOMBRE DE VISITEURS", ROUND(SUM(PAYANT) / SUM(TOTAL) * 100) AS "% PAYANT", ROUND(SUM(GRATUIT) / SUM(TOTAL) * 100) AS "% GRATUIT"
FROM visitors
GROUP BY `NOM DU MUSEE`
ORDER BY 2 DESC
LIMIT 10;

#Query 5: Top 10 Parisian museums in terms of exhibitions average duration

SELECT `Nom officiel du musée`, ROUND(AVG(exhibitions.durée)) AS "Durée moyenne (en jours)"
FROM exhibitions.museums AS museums
LEFT JOIN exhibitions.Paris_exhibitions AS exhibitions
	ON museums.`Nom officiel du musée` = exhibitions.`Nom du lieu`
GROUP BY `Nom officiel du musée`
ORDER BY 2 DESC
LIMIT 10;


