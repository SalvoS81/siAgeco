
INSERT IGNORE INTO agecodbmanager_linea (	
    agecodbmanager_linea.nome,
    agecodbmanager_linea.polo)
	#Seleziona tutte le linee con un polo
	SELECT Linea, Polo FROM
		(
			(
				SELECT DISTINCT t.Linea, IF(t.Monta = 'R8', t.Smonta , t.Monta) as Polo
				FROM estratti AS t			
			)
			UNION
			(
				SELECT DISTINCT t.Linea2, IF(t.Monta2 = 'R8', t.Smonta2 , t.Monta2) as Polo
				FROM estratti AS t
			)
			UNION
			(
				SELECT DISTINCT t.Linea3, IF(t.Monta3 = 'R8', t.Smonta3 , t.Monta3) as Polo
				FROM estratti AS t
			)		
		)AS origincon
	WHERE Polo != 'R8' or (Polo = 'R8' and Linea not in (
    #Seleziona tutte le linee con un polo che non sia R8
		SELECT Linea FROM
		(
			(
				SELECT DISTINCT t.Linea, IF(t.Monta = 'R8', t.Smonta , t.Monta) as Polo
				FROM estratti AS t
				Having Polo != 'R8'
			)
			UNION
			(
				SELECT DISTINCT t.Linea2, IF(t.Monta2 = 'R8', t.Smonta2 , t.Monta2) as Polo
				FROM estratti AS t
				Having Polo != 'R8'
			)
			UNION
			(
				SELECT DISTINCT t.Linea3, IF(t.Monta3 = 'R8', t.Smonta3 , t.Monta3) as Polo
				FROM estratti AS t
				Having Polo != 'R8'
			)		
		) as originsenza        
    )	)
	ORDER BY Linea;
    
    