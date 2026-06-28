WITH tb_compras AS (

    SELECT produto,
        dt_compra,
        avg(valor_produto) AS valor_produto

    FROM compras
    GROUP BY produto, dt_compra

),

tb_lag AS (

    SELECT *,
        lag(dt_compra) OVER (PARTITION BY produto ORDER BY dt_compra) AS dt_ultima_compra
    FROM tb_compras
    ORDER BY produto, dt_compra

),

tb_avg AS (

    SELECT produto,
        avg(julianday(dt_compra) - julianday(dt_ultima_compra)) AS avg_dias_entre_compras

    FROM tb_lag
    GROUP BY produto

),

tb_stats_produto AS (

    SELECT produto,
        max(dt_compra) AS dt_ultima_compra,
        avg(valor_produto) AS media_valor

    FROM compras
    GROUP BY produto

),

tab_final AS (
    SELECT t1.*,
        t2.avg_dias_entre_compras,
        julianday('now') - julianday(t1.dt_ultima_compra) AS dias_desde_ultima_compra

    FROM tb_stats_produto AS t1
    LEFT JOIN tb_avg AS t2
    ON t1.produto = t2.produto
)

SELECT * FROM tab_final;