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
                total_open_positions,
                profiles_submitted,
                interviews_scheduled,
                profiles_not_submitted,
                -- Calculate total_records in the same subquery
                (total_open_positions + profiles_submitted + interviews_scheduled + profiles_not_submitted) AS total_records
            FROM (
                SELECT 
                    (SELECT SUM(dem_positions) 
                    FROM opendemand
                    WHERE dem_dsm_id IN (
                        SELECT dsm_id FROM demandstatusmaster 
                        WHERE dsm_isclosed = 0
                    ) AND dem_isactive = 1) AS total_open_positions,

                    (SELECT COUNT(*) 
                    FROM candidatemaster 
                    WHERE cdm_csm_id IN (
                        SELECT csm_id FROM candidatestatusmaster 
                        WHERE csm_id = '7'
                    ) AND cdm_isactive = 1) AS profiles_submitted,

                    (SELECT COUNT(*) 
                    FROM candidatemaster 
                    WHERE cdm_csm_id IN (
                        SELECT csm_id FROM candidatestatusmaster 
                        WHERE csm_id in( 4,9)
                    ) AND cdm_isactive = 1) AS interviews_scheduled,

                    (SELECT COUNT(*) 
                    FROM candidatemaster 
                    WHERE cdm_csm_id IN (
                        SELECT csm_id FROM candidatestatusmaster 
                        WHERE csm_id IN (1,2,3,4,5)
                    ) AND cdm_isactive = 1) AS profiles_not_submitted
            ) AS counts_table
        ) AS final_counts;

        """)
        row = cursor.fetchone()
    
    return {
        'open_positions': row[0] if row[0] is not None else 0,
        'profiles_submitted': row[1] if row[1] is not None else 0,
        'interview_scheduled': row[2] if row[2] is not None else 0,
        'profiles_not_submitted': row[3] if row[3] is not None else 0
    }

def get_lob_target_progress(): 
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                lm.lob_name,
                TRUNCATE((COUNT(DISTINCT dm.dem_id) * 100.0 / (SELECT COUNT(*) FROM opendemand)), 2) AS demand_percentage  -- Percentage with 2 decimal places
            FROM
                lobmaster lm
            LEFT JOIN
                opendemand dm ON lm.lob_id = dm.dem_lob_id
            GROUP BY
            lm.lob_name

        """)
        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'LOB_name': row[0],
            'percentage': row[1] if row[1] is not None else 0
        })
    return result

def get_demand_data_by_description():
    """Fetch demand data grouped by demand status description and LOB."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                dsm.dsm_code AS category,
                JSON_OBJECTAGG(lob.lob_name, lob_count) AS LOB,
                SUM(lob_count) AS total
            FROM (
                SELECT 
                    od.dem_dsm_id,
                    od.dem_lob_id,
                    COUNT(od.dem_id) AS lob_count
                FROM opendemand od
                GROUP BY od.dem_dsm_id, od.dem_lob_id
            ) AS subquery
            JOIN lobmaster lob ON subquery.dem_lob_id = lob.lob_id
            JOIN demandstatusmaster dsm ON subquery.dem_dsm_id = dsm.dsm_id
            GROUP BY dsm.dsm_code
            ORDER BY dsm.dsm_code;
        """)
        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'category': row[0],
            'LOB': row[1],
            'total': row[2]
        })
    return result

def get_client_selection_percentage():
    with connection.cursor() as cursor:
        cursor.execute("""
            WITH ClientSelection AS (
                SELECT 
                    cm.clm_name AS client_name,  -- Fetch client name instead of generating "Client1", "Client2"
                    COUNT(cdl.cdl_id) AS selected_candidates
                FROM candidatedemandlink cdl
                JOIN opendemand od ON cdl.cdl_dem_id = od.dem_id
                JOIN candidatestatusmaster csm ON cdl.cdl_csm_id = csm.csm_id
                JOIN clientmaster cm ON od.dem_clm_id = cm.clm_id  
                WHERE csm.csm_id = 10  
                GROUP BY cm.clm_name
            ), 
            TotalSelections AS (
                SELECT SUM(selected_candidates) AS total_selected FROM ClientSelection
            ) 
            SELECT 
                cs.client_name,  -- Return actual client name instead of generated "Client1"
                ROUND((cs.selected_candidates * 100.0 / NULLIF(ts.total_selected, 0)), 2) AS selection_percentage
            FROM ClientSelection cs
            JOIN TotalSelections ts ON 1=1
            ORDER BY cs.selected_candidates DESC;
        """)
        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'client_name': row[0],  # Fetch client name
            'selection_percentage': float(row[1])  # Convert percentage to float
        })
    return result



def get_time_taken_for_profile_submission():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT 
        od.dem_id AS demand_id,
        ROUND(AVG(DATEDIFF(cdh.cdh_insertdate, od.dem_insertdate))) AS avg_time_taken
    FROM opendemand od
    JOIN candidatedemandhistory cdh ON od.dem_id = cdh.cdh_dem_id
    WHERE cdh.cdh_csm_id = 7  -- Considering candidates who applied (status 7)
    GROUP BY od.dem_id;
        """)
        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'demand_id': row[0],
            'time_taken': row[1] if row[1] is not None else 0
        })
    
    return result

def get_average_time_taken_for_clients():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                time_taken_sub.client,  
                ROUND(AVG(time_taken_sub.time_taken)) AS avg_time_taken  -- Rounds to the nearest integer
            FROM (
                SELECT 
                    cm.clm_name AS client,  
                    od.dem_id AS demand_id,
                    TIMESTAMPDIFF(DAY, 
                        MIN(cdh.cdh_insertdate), 
                        MAX(cdh.cdh_insertdate)
                    ) AS time_taken
                FROM candidatedemandhistory cdh
                JOIN opendemand od ON cdh.cdh_dem_id = od.dem_id
                JOIN candidatestatusmaster csm ON cdh.cdh_csm_id = csm.csm_id
                JOIN clientmaster cm ON od.dem_clm_id = cm.clm_id
                WHERE csm.csm_id IN (9, 13)
                GROUP BY cm.clm_id, cm.clm_name, od.dem_id  
                HAVING COUNT(DISTINCT csm.csm_id) = 2
            ) AS time_taken_sub
            GROUP BY time_taken_sub.client;
        """)
        rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'client_name': row[0],
            'time_taken': row[1] if row[1] is not None else 0
        })
    
    return result