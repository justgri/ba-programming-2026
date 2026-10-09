1. **Decide what the final output should look like.**
   - Investigate all four datasets and note the messy features: dates without years in 1994-1995, year in sheet names, wide versus long revenues, inconsistent ratings and date formats between the older files and 2013, missing currency information in 2013, different runtime units and conflicting values, absent lookup records, and a missing category.
   - Inspect `rev_US_usd` and `rev_EU_usd`: ask whether amounts are in dollars, thousands, or millions, and what `US` and `EU` mean rather than assuming their market coverage.
   - Define the clean observation as one movie in one market; sketch the clean columns, the two summary tables, and a basic chart.

2. **Plan and apply cleaning specific to each source.**
   - Import `movies_1994` and `movies_1995`; extract `source_year` from each sheet name before concatenating them.
   - Stack those two datasets directly: they have the same column names, rating conventions, and month/day date format.
   - Apply the same cleaning to the combined older data: reconstruct full release dates by combining each month/day value with its `source_year` from the sheet name, then parse the dates.
   - Confirm the older files' metadata: for this classroom example, `US` means USA, `EU` means Europe, and the amounts are millions of USD.
   - Reshape the revenue columns into market and revenue values; map the confirmed market codes to consistent names, keep the USD currency from the headers, and preserve the confirmed million-unit scale.
   - Import `movies_2013`; extract `source_year` from its sheet name.
   - Clean its ratings and parse its month-first dates. Notice that `revenue` specifies neither currency nor units; ask the data provider before combining the amounts. Do not infer currency from market alone.
   - For this classroom exercise, the instructor can confirm that the 2013 USA values are USD and Europe values are EUR, all in millions. Add the confirmed currency information to the data.
   - Make the clean datasets consistent in column names, types, market labels, and units. Preserve the older movies' `runtime_minutes`; leave it missing for 2013 until the lookup is merged.
   - Stack the cleaned datasets together.

3. **Apply joint cleaning to the combined data.**
   - Extract release year and month from the parsed dates; check release year against `source_year`.
   - Once currencies and units have been confirmed, convert revenues to USD using an agreed exchange rate, keeping the amounts in millions. Leave existing USD values unchanged.

4. **Merge the movie lookup.**
   - Check that lookup IDs are unique, then left-join on `movie_id` so all source movies are retained.
   - Identify unmatched movies: D01, The Lion King, and D02, The Jungle Book, have no lookup records. Keep their existing runtime values and flag their missing metadata for follow-up.
   - Convert lookup runtime from hours to minutes into a separate comparison column; compare with the source runtime wherever both are available.
   - Spot the intentional mismatch for D03, Toy Story: the 1995 source says 180 minutes, while the lookup says 1.50 hours, or 90 minutes. Confirm the correct value before resolving the conflict; for this exercise, 180 is the deliberate error.
   - After verification, keep one clean runtime column; use the lookup to supply runtime for the 2013 movies.
   - Spot the missing category for D06, Monsters University; manually fill it with `Animation`.
   - Select the final clean columns, display and export the complete tidy table, and reuse this single dataset unchanged for every summary and chart.

5. **Prepare summary A.**
   - Start from the tidy table and keep only `category`, `release_year`, and `revenue_usd_m` as an intermediate analysis table.
   - Sum USD revenues by category and release year.
   - Keep unresolved categories visible as unknown rather than silently dropping unmatched movies.
   - Reshape with categories as rows and years as columns.

6. **Prepare summary B.**
   - Start again from the same complete tidy table and select `movie_id`, `title`, `market`, and `revenue_usd_m` for the intermediate analysis table.
   - Sum USD revenues by movie and market.
   - Reshape with movies as rows and markets as columns.

7. **Export the clean tables.**
   - Export both summary tables separately from the complete tidy data saved before analysis.

8. **Export a basic chart.**
   - Start again from the same tidy table, select the year, a chosen grouping variable, and revenue, then summarize and plot; label the values as millions of USD.
   - For each analysis, show the same tidy dataset first, the selected columns or grouped totals next, and the resulting summary last.
   - Show how the grouping selector changes the selected columns and totals, and how the chart selector changes the plotting layout.
   - Let the table view switch between equivalent wide and long versions independently of the chart; for these plotting calls, use wide data for grouped bars and long data with explicit year/value/group columns for lines.
