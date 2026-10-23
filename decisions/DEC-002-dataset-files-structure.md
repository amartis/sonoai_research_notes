# Definition

Training dataset or simply dataset is the dataset fed into training session.

# Higher Level Concepts

dataset version - the versioning of dataset content
dataset style - the encryption, folder structure (plainified or structured) style of dataset
dataset - has content version and content style defined, and the content.
dataset codename - the combination of dataset version and style - unique identifier of the dataset
dataset components - regardless of the version and style, the content is composed in certain structure with defined component types which are described in [Content Components](#content-components) section.

# Dataset Components

- image files, accompanied with taskcrops_df
    - image files can be in plain or encrypted form
        - if encrypted the encryption word should be in credential file of SONOAI_DATA_KEY_FILE
- taskcrops_df.pkl
    defines the cropping area (in the image) for each training sample, and other important meta information of the images (width, height, md5 value, ...)
- labeling dataframes - flags, polygons, texts

# Dataset version, style, codename

- version : YYMMDD
- style : human readable name (can be short as the dataset has style)

## Codename of data version+style

Codename Convention: YYMMDD_alphabetname
Example: 261022_submit1


{data_files_root}
    |- dataset_styles (Note 1)
        |- style1.md
        |- style2.md
        |- ...
    |- datasets
        |- {dataset-codename}
            |- style 
            |- images/
                |- image files in plain structure or in hierarchies (Note 2)
                |- taskcrops_df.pkl (Note 3)
            |- labels/
                |- flags_df.pkl
                |- polygons_df.pkl
                |- texts_df.pkl

Note 1:
explains the details of the data version - encryptions, decisions made for the version, etc ; credendtials of encryption should be kept in proper folder of the project codebase ; this should never be pushed to any server

Note 2:
The image files can be replaced with softlink or hardlink or text files with relative or absolute path to the image files of another dataset folder

Note 3:
Additional information can be fed in two styles:
First style, taskcrops_df.pkl may have additional columns like datasource_id
Second style, additional dataframe pkl file is accompanied to taskcrops_df.pkl