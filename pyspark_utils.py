from pyspark.sql import DataFrame, Column
from pyspark.sql import functions as F

def agg_entropy(
    df: DataFrame,
    group_columns: list[str] | list[Column],
    category_column: str | Column
    ) -> DataFrame:
    
    category_agg = df.groupby(group_columns, category_column).count()
    group_agg = (
        category_agg
        .groupby(group_columns)
        .agg(
            F.sum('count').alias('total_count'),
        )
    )
    category_agg = category_agg.join(group_agg, on=group_columns)
    category_agg = category_agg.withColumn(
        'probability',
        F.col('count') / F.col('total_count')
    )
    category_agg = category_agg.withColumn(
        'term',
        -F.col('probability') * F.log2('probability')
    )
    df_agg = (
        category_agg
        .groupby(group_columns)
        .agg(
            F.sum('term').alias('entropy'),
            F.count(category_column).alias('n_categories')
        )
    )
    df_agg = df_agg.withColumn(
        'norm_entropy',
        F.col('entropy') / F.log2('n_categories')
    )
    return df_agg
