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

def get_open_demand_data():
    """Fetch open demand statistics including India and Non-India counts"""
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH StatusMapping AS (
                SELECT dsm_id 
                FROM demandstatusmaster 
                WHERE dsm_code = 'Open'
            )
            SELECT 
                (SELECT COUNT(*) 
                 FROM opendemand 
                 WHERE dem_dsm_id IN (SELECT dsm_id FROM StatusMapping)) AS total_open_demands,

                (SELECT COUNT(*) 
                 FROM opendemand 
                 WHERE dem_dsm_id NOT IN (SELECT dsm_id FROM StatusMapping)) AS total_non_open_demands,

                (SELECT COUNT(*) 
                 FROM opendemand od
                 JOIN locationmaster lm ON od.dem_lcm_id = lm.lcm_id
                 WHERE od.dem_dsm_id IN (SELECT dsm_id FROM StatusMapping)
                   AND lm.lcm_country = 'India') AS total_india_open_demands,

                (SELECT COUNT(*) 
                 FROM opendemand od
                 JOIN locationmaster lm ON od.dem_lcm_id = lm.lcm_id
                 WHERE od.dem_dsm_id IN (SELECT dsm_id FROM StatusMapping)
                   AND lm.lcm_country != 'India') AS total_non_india_open_demands;
        """)
        row = cursor.fetchone()

    return {
        'total_open_demands': row[0] if row[0] is not None else 0,
        'total_non_open_demands': row[1] if row[1] is not None else 0,
        'total_india_open_demands': row[2] if row[2] is not None else 0,
        'total_non_india_open_demands': row[3] if row[3] is not None else 0
    }

def get_total_positions_opened_last_week():
    """Fetch the total number of positions opened last week"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                SUM(dem_positions) AS total_positions_opened
            FROM opendemand
            WHERE dem_insertdate >= DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 7 DAY)
              AND dem_insertdate < DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) + 1 DAY)
              AND dem_isactive = 1
              AND dem_dsm_id in (1,2,3);
        """)
        row = cursor.fetchone()
    
    return {'total_positions_opened_last_week': int(row[0]) if row[0] is not None else 0}

def get_demand_fulfillment_metrics():
    """Fetch percentage data for open positions, profiles submitted, interviews scheduled, and profiles not submitted."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                CAST((total_open_positions * 100.0 / total_records) AS DECIMAL(5, 2)) AS open_positions,
                CAST((profiles_submitted * 100.0 / total_records) AS DECIMAL(5, 2)) AS profiles_submitted,
                CAST((interviews_scheduled * 100.0 / total_records) AS DECIMAL(5, 2)) AS interview_scheduled,
                CAST((profiles_not_submitted * 100.0 / total_records) AS DECIMAL(5, 2)) AS profiles_not_submitted
            FROM (
                SELECT
                    (SELECT SUM(dem_positions)
                     FROM opendemand
                     WHERE dem_dsm_id IN (SELECT dsm_id FROM demandstatusmaster WHERE dsm_code IN ('Open', 'Req Not Clear', 'JD Not Received'))
                     AND dem_isactive = 1) AS total_open_positions,
    
                    (SELECT COUNT(*)
                     FROM candidatemaster
                     WHERE cdm_csm_id IN (SELECT csm_id FROM candidatestatusmaster WHERE csm_code = 'Sent to Client')
                     AND cdm_isactive = 1) AS profiles_submitted,
    
                    (SELECT COUNT(*)
                     FROM candidatemaster
                     WHERE cdm_csm_id IN (SELECT csm_id FROM candidatestatusmaster WHERE csm_code IN ('Interview Scheduled', 'L1 Scheduled', 'Client Interview Scheduled'))
                     AND cdm_isactive = 1) AS interviews_scheduled,
    
                    (SELECT COUNT(*)
                     FROM candidatemaster
                     WHERE cdm_csm_id IN (SELECT csm_id FROM candidatestatusmaster WHERE csm_code IN ('Applied', 'Screening', 'Shortlisted', 'Interview Scheduled', 'L1 Scheduled'))
                     AND cdm_isactive = 1) AS profiles_not_submitted,
    
                    (SELECT 
                        (SELECT SUM(dem_positions)
                         FROM opendemand
                         WHERE dem_dsm_id IN (SELECT dsm_id FROM demandstatusmaster WHERE dsm_code IN ('Open', 'Req Not Clear', 'JD Not Received'))
                         AND dem_isactive = 1) +
                        (SELECT COUNT(*)
                         FROM candidatemaster
                         WHERE cdm_csm_id IN (SELECT csm_id FROM candidatestatusmaster WHERE csm_code = 'Sent to Client')
                         AND cdm_isactive = 1) +
                        (SELECT COUNT(*)
                         FROM candidatemaster
                         WHERE cdm_csm_id IN (SELECT csm_id FROM candidatestatusmaster WHERE csm_code IN ('Interview Scheduled', 'L1 Scheduled', 'Client Interview Scheduled'))
                         AND cdm_isactive = 1) +
                        (SELECT COUNT(*)
                         FROM candidatemaster
                         WHERE cdm_csm_id IN (SELECT csm_id FROM candidatestatusmaster WHERE csm_code IN ('Applied', 'Screening', 'Shortlisted', 'Interview Scheduled', 'L1 Scheduled'))
                         AND cdm_isactive = 1)
                    ) AS total_records  -- Total number of all records.
            ) AS subquery;
        """)
        row = cursor.fetchone()
    
    return {
        'open_positions': row[0] if row[0] is not None else 0,
        'profiles_submitted': row[1] if row[1] is not None else 0,
        'interview_scheduled': row[2] if row[2] is not None else 0,
        'profiles_not_submitted': row[3] if row[3] is not None else 0
    }