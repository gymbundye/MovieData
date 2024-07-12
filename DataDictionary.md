## Data Dictionary

### Movie Dataset

1. **Movie Name**
   - **Description**: The title of the movie.
   - **Data Type**: Text (String).
   - **Format**: Variable character length.
   - **Constraints**: None.
   - **Example**: "The Shawshank Redemption".

2. **Picked By**
   - **Description**: User who picked or rated the movie.
   - **Data Type**: Text (String).
   - **Format**: Variable character length.
   - **Constraints**: Must be one of 'jon', 'jim', or 'phill'.
   - **Example**: "jon".

3. **Avg Rating**
   - **Description**: Average rating given to the movie by the user.
   - **Data Type**: Numeric (Float).
   - **Format**: Decimal number from 1 to 10.
   - **Constraints**: Must be between 1 and 10.
   - **Example**: 8.5.

4. **Date**
   - **Description**: Date when the movie was picked or rated.
   - **Data Type**: Text (String) or Date format.
   - **Format**: YYYY-MM-DD.
   - **Constraints**: Must be a valid date format.
   - **Example**: "2023-05-15".

5. **TMDB_ID**
   - **Description**: The Movie Database (TMDB) ID of the movie.
   - **Data Type**: Integer.
   - **Format**: Numeric.
   - **Constraints**: None.
   - **Example**: 278 (TMDB ID for "The Shawshank Redemption").

6. **Overview**
   - **Description**: Brief overview or synopsis of the movie.
   - **Data Type**: Text (String).
   - **Format**: Variable character length.
   - **Constraints**: None.
   - **Example**: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."

7. **Genres**
   - **Description**: Genres associated with the movie.
   - **Data Type**: Text (String).
   - **Format**: Comma-separated list of genres.
   - **Constraints**: None.
   - **Example**: "Drama, Crime".

8. **Release Date**
   - **Description**: Date when the movie was released.
   - **Data Type**: Text (String) or Date format.
   - **Format**: YYYY-MM-DD.
   - **Constraints**: Must be a valid date format.
   - **Example**: "1994-09-10".

9. **Vote Average**
   - **Description**: Average rating of the movie on TMDB.
   - **Data Type**: Numeric (Float).
   - **Format**: Decimal number from 0 to 10.
   - **Constraints**: Must be between 0 and 10.
   - **Example**: 8.7.

10. **Vote Count**
    - **Description**: Number of votes received on TMDB for the movie.
    - **Data Type**: Integer.
    - **Format**: Numeric.
    - **Constraints**: None.
    - **Example**: 18868.

11. **TMDb Link**
    - **Description**: URL link to the movie on TMDB.
    - **Data Type**: Text (String).
    - **Format**: URL format.
    - **Constraints**: None.
    - **Example**: "https://www.themoviedb.org/movie/278".

12. **Running Time**
    - **Description**: Duration of the movie in minutes.
    - **Data Type**: Integer.
    - **Format**: Numeric.
    - **Constraints**: None.
    - **Example**: 142.
