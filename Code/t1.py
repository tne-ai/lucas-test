import pandas as pd
from typing import Optional

def t1(
        query: str,
        ebp_trendcaster_product_assortment: [pd.DataFrame] = None,
        session_id: Optional[str] = "") -> str:

    #Remove rows of duplicate Style Color
    upf = ebp_trendcaster_product_assortment.drop_duplicates(subset = 'Style Color')

    # Filter to Date = September
    sept_all_cats = upf[upf['Date'] == "September"]

    #Group by Retailer and count Style Color
    all_results_df = sept_all_cats.groupby('Retailer')['Style Color'].count().reset_index()

    # Set column labels
    all_results_df.columns = ['Retailer', 'All Categories']
    sept_coats = sept_all_cats[sept_all_cats['Category'] == 'Coats']

    # Group by Retailer and count Style Color
    coats_results_df = sept_coats.groupby("Retailer")['Style Color'].count().reset_index()
    coats_results_df.columns = ['Retailer', 'Coats']

    # Merge All and Categories DataFrames
    side_by_side = coats_results_df.merge(all_results_df, on="Retailer", how='left')

    # Do sum of numeric fields
    sums = side_by_side.sum(numeric_only=True)

    # Make sums a DataFrame
    sums_df = pd.DataFrame([sums], index=['Total'])

    # Reset index of side_by_side to Retailer
    side_by_side = side_by_side.set_index('Retailer')

    # Append sums to main dataframe
    side_by_side = pd.concat([side_by_side, sums_df])

    # Add percentage column to side_by_side
    side_by_side['Coats Percentage'] = (side_by_side['Coats'] / side_by_side['All Categories'] * 100).round(1)

    transposed_side_by_side = side_by_side.transpose()

    ## Reorder columns to be MK first, then competitors alphabetized
    # Check if 'Moose Knuckles' is in the columns
    if 'Moose Knuckles' in transposed_side_by_side.columns:
        # 'Moose Knuckles' is present, so it's put first, followed by the rest sorted alphabetically
        columns_ordered = ['Moose Knuckles'] + sorted(
            [col for col in transposed_side_by_side.columns if col != 'Moose Knuckles'])
    else:
        # 'Moose Knuckles' is not present, so just sort all columns alphabetically
        columns_ordered = sorted(transposed_side_by_side.columns)

    # Reorder the DataFrame columns using the custom list
    transposed_side_by_side = transposed_side_by_side[columns_ordered]

    return transposed_side_by_side.to_markdown()