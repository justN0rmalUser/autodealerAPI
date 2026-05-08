from dataclasses import dataclass

@dataclass(frozen=True)
class GOODS_IN:
    GET_GOODS_IN_ID_BY_SHOP_NOM_ABSOLUTE = """SELECT
        GOODS_IN_ID,
        SHOP_NOMENCLATURE_ID,
        CODE,
        PRODUCER_ID
    FROM GOODS_IN
    LEFT JOIN DOCUMENT_IN USING(DOCUMENT_IN_ID)
    LEFT JOIN SHOP_NOMENCLATURE USING(SHOP_NOMENCLATURE_ID)
    WHERE (DATE_REGISTRATION < ? 
        AND DATE_REGISTRATION > ?
        AND COST1 = ?
        AND STATE = 4 
        AND ORGANIZATION_ID = 1 
        AND PROVIDER_ID = 5 
        AND SHOP_NOMENCLATURE_ID IN {snids}
        AND IS_SALED = ?)
    ORDER BY GOODS_IN_ID DESC;
    """
    GET_GOODS_IN_ID_BY_SHOP_NOM_CLOSE = """SELECT
        GOODS_IN_ID,
        SHOP_NOMENCLATURE_ID,
        CODE,
        PRODUCER_ID
    FROM GOODS_IN
    LEFT JOIN DOCUMENT_IN USING(DOCUMENT_IN_ID)
    LEFT JOIN SHOP_NOMENCLATURE USING(SHOP_NOMENCLATURE_ID)
    WHERE (DATE_REGISTRATION < ? 
        AND DATE_REGISTRATION > ?
        AND STATE = 4 
        AND ORGANIZATION_ID = 1 
        AND PROVIDER_ID = 5 
        AND SHOP_NOMENCLATURE_ID IN {snids}
        AND IS_SALED = ?)
    ORDER BY GOODS_IN_ID DESC;
    """


@dataclass(frozen=True)
class Other:
    GET_FREE_CELLS = """SELECT
        COALESCE(
            (SELECT MAX(gin.GOODS_COUNT) FROM GOODS_IN gin WHERE gin.GOODS_IN_ID = ?), 0
        ) -
        COALESCE(
            SUM(
                CASE
                    WHEN got.GOODS_COUNT_FACT = got.GOODS_COUNT
                        THEN got.GOODS_COUNT_FACT - COALESCE(got.GOODS_COUNT_RETURN, 0)
                    ELSE got.GOODS_COUNT
                END
            ), 0
        ) AS FREE_CELLS
    FROM GOODS_OUT got
    INNER JOIN DOCUMENT_OUT dout ON dout.DOCUMENT_OUT_ID = got.DOCUMENT_OUT_ID
    WHERE got.GOODS_IN_ID = ? AND dout.DOCUMENT_TYPE_ID IN (2, 7, 11);
    """
    
    GET_NUMBER_FOR_DOC_OUT = 'SELECT COALESCE(MAX("NUMBER"), 0) + 1 FROM DOCUMENT_OUT_HEADER WHERE DOCUMENT_TYPE_ID = 7'
    
    

@dataclass(frozen=True)
class FindProduct:
    GET_SNID_SQL = """SELECT SNID
    FROM identify_product
    FULL JOIN firm f USING(FIRM_ID)
    inner join code c USING(CODE)
    WHERE f.FORMATTED_NAME = ? AND c.FORMATTED_CODE = ?
    ORDER BY SNID DESC
    """

    SEEK_FIRM_BY_RAW = "SELECT FIRM_ID FROM firm WHERE FORMATTED_NAME = ?"
    SEEK_FIRM_BY_SNID = "SELECT FIRM_ID FROM identify_product WHERE SNID = ?"

    SEEK_CODE_BY_RAW = "SELECT CODE FROM code WHERE FORMATTED_CODE = ?"
    SEEK_CODE_BY_SNID = "SELECT CODE FROM identify_product WHERE SNID = ?"


