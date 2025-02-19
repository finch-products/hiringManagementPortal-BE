from django.db import connection

def get_age_demand_data():
    with connection.cursor() as cursor:
        cursor.execute("""         
            SELECT
                CASE
                    WHEN TIMESTAMPDIFF(DAY, d.dem_ctooldate, 
                        COALESCE(dh.dhs_dsm_insertdate, d.dem_validtill)
                    ) < 20 THEN '<20'
                    WHEN TIMESTAMPDIFF(DAY, d.dem_ctooldate, 
                        COALESCE(dh.dhs_dsm_insertdate, d.dem_validtill)
                    ) BETWEEN 20 AND 29 THEN '20-29'
                    WHEN TIMESTAMPDIFF(DAY, d.dem_ctooldate, 
                        COALESCE(dh.dhs_dsm_insertdate, d.dem_validtill)
                    ) BETWEEN 30 AND 39 THEN '30-39'
                    WHEN TIMESTAMPDIFF(DAY, d.dem_ctooldate, 
                        COALESCE(dh.dhs_dsm_insertdate, d.dem_validtill)
                    ) BETWEEN 40 AND 49 THEN '40-49'
                    WHEN TIMESTAMPDIFF(DAY, d.dem_ctooldate, 
                        COALESCE(dh.dhs_dsm_insertdate, d.dem_validtill)
                    ) BETWEEN 50 AND 59 THEN '50-59'
                    ELSE '60+'
                END AS age,
                SUM(COALESCE(dc.candidate_count, 0)) AS candidate_count
            FROM opendemand d
            LEFT JOIN demandhistory dh 
                ON d.dem_id = dh.dhs_dem_id AND dh.dhs_todata LIKE '%Closed%'
            LEFT JOIN (
                SELECT cdl_dem_id, COUNT(*) AS candidate_count
                FROM candidatedemandlink
                GROUP BY cdl_dem_id
            ) dc ON d.dem_id = dc.cdl_dem_id
            GROUP BY age
            ORDER BY age;
        """)
        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'age': row[0],
            'count': row[1] if row[1] is not None else 0  # Ensures None is replaced with 0
        })
    return result