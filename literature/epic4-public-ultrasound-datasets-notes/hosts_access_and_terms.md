# Download hosts for public ultrasound datasets: access methods, limits and terms (as of 2026-11-26)

Scope and method. These notes cover hosts and agreements only, not individual datasets. Sources were read on 2026-11-25 and 2026-11-26. "Observed" means a check I ran myself from machine01, the project's local workstation, which is not an AWS address. Each check used curl and read only HTTP headers or small JSON metadata. Nothing was downloaded, no account was created, used or logged into, and no terms were accepted. Statements about terms are my reading, not legal advice. Roboflow is out of scope; [DEC-081](../../decisions/DEC-081-epic2-mission-roboflow-universe-ultrasound-scraper.md) and [DEC-096](../../decisions/DEC-096-epic2-retrieval-path-official-routes-terms-reading-fetch-budget.md) (the project's epic 2 decisions on Roboflow) cover it.

Abbreviations:
- API: application programming interface. CLI: command-line tool.
- ToS: terms of service. DUA: data use agreement. RUA: research use agreement.
- PAT: personal access token.
- SAS: shared access signature, an Azure URL that carries a signed token.
- WAF: web application firewall, a bot filter.
- LFS: Git Large File Storage.
- ODR: the AWS Open Data Registry.
- IDC: NCI Imaging Data Commons. CRDC: NCI Cancer Research Data Commons.
- dbGaP: the NIH database that runs controlled access. DAR: dbGaP data access request. DUC: NIH data use certification.
- NBIA: the older TCIA download software. TDR: the new TCIA Data Retriever.
- EC2: AWS virtual machines. S3: AWS object storage.
- CC BY, CC BY-NC, CC BY-NC-SA: Creative Commons licences; NC means non-commercial and SA means share-alike.

## 1. For each host: the official tool, the exact download method, the authentication needed, and how to give a token to a server safely

### Takeaway
Most open repositories have a documented HTTP API or CLI that works with no login. These are Zenodo, figshare, Harvard Dataverse, OSF, PhysioNet open projects, TCIA open collections and IDC, the AWS ODR, Hugging Face public datasets, GitHub and the CAMUS Girder database. A token or account cookie is needed for the following:
- Kaggle.
- Hugging Face gated datasets.
- Synapse, even for open data.
- Grand Challenge archives.
- Stanford AIMI, which now serves its datasets through Redivis rather than Azure.
- IEEE DataPort, where AWS keys come with a subscription.
- Dryad file downloads, in practice.
- Baidu Netdisk.

On every host that documents it, the token goes in an HTTP header or an environment variable, not in the URL.

### Cited Findings

Table 1. Per-host download route and authentication. This is a summary; the details and sources are in the bullets below the table. "None" means no login is needed for public items.

| Host | Official route (tool or API) | Authentication |
|---|---|---|
| Zenodo | REST API record JSON lists each file with a link, a size and an md5; `zenodo_get` CLI | None for open records; OAuth or PAT as `Authorization: Bearer` |
| figshare | API v2 `/articles/{id}/files` gives `download_url` (ndownloader) | None for public items; `Authorization: token` |
| Mendeley Data | "Mendeley Data public API" (docs not readable, see gaps) | Unclear |
| Kaggle | `kaggle` CLI: `datasets download`, `competitions download` | API token; competition rules accepted on the website first |
| Hugging Face | `hf download`, `huggingface_hub` | None for public; `HF_TOKEN` for gated, after a browser request |
| GitHub | git clone (with LFS), REST API, release assets | None for public; a PAT raises the API limit |
| Google Drive | Drive API `files.get` with `alt=media`; rclone `drive`; gdown | OAuth for the API and rclone; browser cookies optional for gdown |
| OneDrive / SharePoint | Microsoft Graph `shares` API | Always an authenticated user (Business and SharePoint) |
| Dropbox | shared links; rclone `dropbox` | Link owner's limits apply (see Q2) |
| Baidu Netdisk | BaiduPCS-Go (third-party) | Account cookies (BDUSS, STOKEN) |
| Grand Challenge | `gcapi` Python client for archives; challenge data often on Zenodo or the AWS ODR | API token from profile, plus an access grant per archive |
| TCIA | TDR (new), NBIA Data Retriever (old), `tcia_utils`; IDC buckets for public DICOM | None for open data; dbGaP approval plus CRDC credentials for controlled data |
| PhysioNet | `wget -r -N -c -np`, `physionet` Python package, `aws s3 sync` | None for open data; credentialed account plus a signed DUA for credentialed data |
| Stanford AIMI | Redivis (web, REST API, Python client) | Redivis account plus data-access approval; API token |
| Synapse | `synapseclient` (`synapse get -r`) | Account always; PAT via `SYNAPSE_AUTH_TOKEN` |
| IEEE DataPort | website; S3 bucket `ieee-dataport` with AWS keys | IEEE account; subscription for AWS keys |
| Science Data Bank | website; OAI-PMH metadata | Login for some files (see gaps) |
| Harvard Dataverse | Dataverse Data Access API | None for public files; `X-Dataverse-key`; a guestbook POST when a guestbook is set |
| Dryad | API v2 | Anonymous use is limited; an API-account token lasts 10 hours |
| OSF | API v2 | Optional token raises the rate limit |
| Academic Torrents | BitTorrent (Transmission, aria2c), web seeds | None |
| AWS ODR | `aws s3` with `--no-sign-request` | None; AWS credentials for requester-pays buckets |
| CREATIS (CAMUS) | Girder database REST API | None (collection marked public) |
| On request by email | none | manual |

#### Zenodo
- Zenodo supports OAuth 2.0 and personal access tokens. The recommended method is the `Authorization: Bearer <ACCESS_TOKEN>` header; an `access_token` URL parameter is allowed but described as less secure — [Zenodo developers](https://developers.zenodo.org/).
- The record JSON of a public record lists each file with the keys `checksum`, `id`, `key`, `links` (a `self` link) and `size`. The checksum has the form `md5:<hash>`. Observed on 2026-11-26 with no token, at `https://zenodo.org/api/records/<id>` for one public record — [example record API](https://zenodo.org/api/records/1327317).
- `zenodo_get`: `uvx zenodo_get RECORD_ID_OR_DOI`. Flags: `-m` writes `md5sums.txt`, `-R N` sets checksum retries, `-p N` sets the pause, `--max-http-retries N` uses exponential backoff, and `-w FILE` writes the URL list instead of downloading (input for aria2c `-i`) — [zenodo_get README](https://github.com/dvolgyes/zenodo_get).

#### figshare
- The API accepts OAuth or personal tokens. The preferred method is the header `Authorization: token ACCESS_TOKEN`; a `?access_token=` parameter also works. API v3 adds item-type metadata, and tokens are not tied to a version — [figshare API docs](https://docs.figshare.com/).
- Observed on 2026-11-25 with no token: `https://api.figshare.com/v2/articles/{id}/files` returned HTTP 200. Each file entry has `computed_md5`, `supplied_md5`, `download_url`, `is_link_only`, `mimetype`, `name` and `size`. A HEAD request on a `download_url` (ndownloader) returned HTTP 302 to a `*.r2.cloudflarestorage.com` address, so file storage now sits behind Cloudflare R2. `Accept-Ranges` and `Content-Range` were listed in `access-control-expose-headers` — [figshare API](https://api.figshare.com/v2/articles?page_size=1).
- Figshare says all publicly published content can be downloaded by anyone with no login. I saw this in a search summary only, not on a page I read — [figshare info page](https://info.figshare.com/?p=2658).

#### Mendeley Data
- Elsevier says that "external systems are also able to query and download any published and valid dataset via the Mendeley Data public API". I saw this in a search summary only — [Mendeley Data archive process](https://data.mendeley.com/archive-process).
- Per Elsevier support, the API docs are at data.mendeley.com/api/docs/. Search summary only — [Elsevier support](https://www.elsevier.support/mendeley/answer/can-i-manage-my-datasets-in-mendeley-data-repository-via-an-api).
- Observed: data.mendeley.com is served by Cloudflare (`server: cloudflare`). The terms page is a JavaScript app that returns no text to curl. A guessed path `/public-api/datasets` returned 404, so I could not confirm the endpoint — [Mendeley Data](https://data.mendeley.com/terms).
- Personal accounts are limited to 10 GB per dataset (search summary) — [Harvard Medical School data management](https://datamanagement.hms.harvard.edu/share/data-repositories/mendeley-data).

#### Kaggle
- Authentication options:
  - `kaggle auth login`, a web-based OAuth flow.
  - The `KAGGLE_API_TOKEN` environment variable.
  - A token file at `~/.kaggle/access_token`.
  - The legacy `~/.kaggle/kaggle.json` (a "Legacy API Key").
  - The CLI requires Python 3.11 or later — [Kaggle API docs](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md).
- Commands are `kaggle datasets download <owner/dataset[/version]> [-f FILE] [-p PATH] [--unzip] [-o] [-q]` and `kaggle competitions download <COMPETITION> [-f FILE] [-p PATH] [--unzip] [-o]` — [datasets.md](https://github.com/Kaggle/kaggle-api/blob/main/docs/datasets.md), [competitions.md](https://github.com/Kaggle/kaggle-api/blob/main/docs/competitions.md).
- Competition data needs the rules accepted on the website first. Users also report phone verification before the accept button works. This is forum evidence only, so unverified — [fast.ai forum](https://forums.fast.ai/t/unable-to-download-bluebook-for-bulldozers-with-kaggle-api/32640).

#### Hugging Face
- For gated datasets you must be logged in. "Requesting access can only be done from your browser." After approval, scripts download with a user token (`hf auth login`, or the `token` argument) — [HF gated datasets](https://huggingface.co/docs/hub/datasets-gated).
- Download commands are `hf download <repo>` and `hf download hf://datasets/<id>`, with `--include` and `--dry-run`; `snapshot_download(repo_id, repo_type="dataset")` does the same from Python. `hf_xet` has been installed with `huggingface_hub` since version 0.32.0. "`hf_transfer` ... is now deprecated; use `hf_xet` instead" — [HF download guide](https://huggingface.co/docs/huggingface_hub/guides/download).
- "Make sure you always pass a `HF_TOKEN`" to avoid rate limits — [HF rate limits](https://huggingface.co/docs/hub/rate-limits).

#### GitHub
- Unauthenticated REST calls are limited per IP address. A PAT gives a personal limit (numbers in Q2) — [GitHub REST rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api).
- Git LFS downloads count against the repository owner's bandwidth (details in Q2) — [GitHub LFS storage and bandwidth](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-storage-and-bandwidth-usage).

#### Google Drive
- "To download a blob file stored on Drive, use the files.get method with the ID of the file". Downloads "must be authorized with a scope that allows read access to the file content". The page does not mention API keys. Partial downloads use a `Range` header. `acknowledgeAbuse=true` is needed for files flagged as abusive — [Drive API downloads](https://developers.google.com/workspace/drive/api/guides/manage-downloads).
- rclone `drive` backend:
  - It reaches shared folders through `--drive-root-folder-id` and `--drive-shared-with-me`.
  - Some old files need a resource key.
  - "The shared client_id is being retired and will stop working during 2026, so creating your own is now strongly recommended."
  - Unattended use is possible with service accounts — [rclone drive](https://rclone.org/drive/).
- gdown downloads public files and folders. It reuses cookies from `~/.cache/gdown/cookies.txt` or `--cookies-from-browser`, resumes with `--continue` and limits speed with `--speed` — [gdown README](https://github.com/wkentaro/gdown).

#### OneDrive and SharePoint
- "For OneDrive for Business and SharePoint, the Shares API always requires authentication and can't be used to access anonymously shared content without a user context." The least-privileged permission is Files.ReadWrite (delegated) — [Microsoft Graph shares-get](https://learn.microsoft.com/en-us/graph/api/shares-get).
- Users report that appending `download=1` to an "Anyone" link makes curl or wget fetch the file, but not on every SharePoint site. Forum evidence only, so unverified — [Microsoft Tech Community thread](https://techcommunity.microsoft.com/t5/onedrive-for-business/get-direct-download-link-of-a-file-in-onedrive-for-business/td-p/149766), [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5384212/how-to-generate-directly-download-link-from-the-sh).

#### Dropbox
- Shared links are public URLs, and the link owner's daily traffic limits apply (see Q2) — [Dropbox banned links](https://help.dropbox.com/share/banned-links).
- Changing `dl=0` to `dl=1` to force a direct download is common practice, but I did not verify it at a source — unverified.

#### Baidu Netdisk
- BaiduPCS-Go logs in with browser cookies (`login -cookies=...`, recommended) or with `-bduss=<BDUSS> -stoken=<STOKEN>`. The STOKEN must come from the Netdisk page. Password login is "long unmaintained".
- `download <path>` fetches your own files. `transfer <share link> <extraction code>` copies a share into your own Netdisk first.
- Latest release: v4.0.2, dated 2026-08-21 — [BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go).
- Signing up reportedly needs a mainland-China phone number for most countries. This comes from one forum post (2026-09-08) by an author who sells a download service, so unverified — [HF forum post](https://discuss.huggingface.co/t/how-to-download-from-baidu-pan-pan-baidu-com-without-a-chinese-account-2026-notes-for-datasets-a-free-fetcher/180125).

#### Grand Challenge
- Make a personal token in the profile under "Manage API Tokens"; it is shown only once. Then run `gcapi.Client(token=...)`, find an archive by its slug, and call `client.images.download`. Archive access must be granted. All of this comes from search summaries of the official docs and PyPI — [GC-API for archives](https://grand-challenge.org/documentation/gc-api-for-archives), [gcapi on PyPI](https://pypi.org/project/gcapi/).
- A forum user got only the first 100 images from an archive, so the listing is paginated — [Grand Challenge forum](https://grand-challenge.org/forums/forum/general-548/topic/download-more-than-100-images-from-archive-1596).
- Organisers are told: "We recommend using either Zenodo or the AWS Open Data Registry to make your training data publicly available to participants." The page notes Zenodo's "50 GB size limit per repository" — [Grand Challenge data storage](https://grand-challenge.org/documentation/data-storage/).

#### TCIA
- TCIA's download page introduces "TCIA Data Retriever" as a new application that "will download our datasets regardless of where they reside". It says "Please upgrade to TCIA Data Retriever as soon as possible". The legacy NBIA Data Retriever is at version 4.4.3, and its Linux CLI "does not require the desktop environment" — [TCIA download page](https://wiki.cancerimagingarchive.net/display/NBIA/Downloading+TCIA+Images).
- A search snippet of the same page says: "As of March 2026, TCIA is in the process of a major infrastructure update. We will be deprecating our NBIA software ... over the coming year". This came from the search engine only; my fetch of the page did not show it.
- TDR is a "cross-platform desktop GUI (and CLI)":
  - `--cli` runs it with no GUI.
  - It reads `.tcia`, `.s5cmd`, spreadsheet and Croissant manifests.
  - `--auth` takes a CRDC/Gen3 JSON credentials file.
  - MD5 validation is on by default.
  - Resume uses "skip-existing logic", and "Aspera handoffs are skipped" — [TDR on GitHub](https://github.com/TCIA/data-retriever).
- `tcia_utils` v4 (preview 4.0.0a19) offers `download_dataset()`, `download_manifest()` and `download_files()`. It accepts `.tcia` files or CSV/TSV with a `SeriesInstanceUID`, `imageUrl` or `drs_uri` column. "TDR owns downloads, retries, verification, authorization" and "Keys are required for controlled DRS transfers" — [tcia_utils](https://github.com/kirbyju/tcia_utils).
- IDC public DICOM data is in the S3 buckets `idc-open-data` (CC BY), `idc-open-data-two` (CC BY-NC) and `idc-open-data-cr`, all in us-east-1. Access is `aws s3 ls --no-sign-request s3://<bucket>/`, with updates every 1 to 3 months — [AWS ODR: IDC](https://registry.opendata.aws/nci-imaging-data-commons/).

#### PhysioNet
- An open project page offers four routes: "Download the ZIP file", `physionet download ptb-xl --version 1.0.3`, `wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/` and `aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ DESTINATION` — [PhysioNet PTB-XL page](https://physionet.org/content/ptb-xl/1.0.3/).
- A credentialed project page reads: "Only credentialed users who sign the DUA can access the files". The licence is "PhysioNet Credentialed Health Data License 1.5.0" and the required training is "CITI Data or Specimens Only Research" — [MIMIC-IV page](https://physionet.org/content/mimiciv/3.1/).
- The usual credentialed form is `wget ... --user <name> --ask-password`. This is unverified, because the files section is hidden when logged out.
- Cloud access works by linking an AWS identifier in the PhysioNet profile's Cloud section and then requesting access on the project page (search summaries) — [MIMIC cloud linking](https://mimic.mit.edu/docs/gettingstarted/cloud/link), [PhysioNet FAQ](https://physionet.org/about/faqs/).
- A PhysioNet developer note says "An AWS account ID is not an identity" and proposes a signed-URL check, so the linking steps may have changed (search summary) — [physionet-build PR 2121](https://www.github.com/MIT-LCP/physionet-build/pull/2121).

#### Stanford AIMI
- AIMI now says researchers "download data directly through Redivis" and links to https://stanford.redivis.com/AIMI — [AIMI shared datasets](https://aimi.stanford.edu/shared-datasets).
- Observed on 2026-11-26 with no token: the Redivis API lists 38 AIMI datasets — [Redivis API listing](https://redivis.com/api/v1/organizations/AIMI/datasets?maxResults=50).
  - Seven are ultrasound or echo datasets: EchoNet-Dynamic, EchoNet-Pediatric, EchoNet-LVH, EchoNet-TEE-View-Classifier, Thyroid Ultrasound Cine-clip, MRI-Ultrasound Prostate and CT2Echo.
  - The one I read in full (EchoNet-Pediatric, 2.51 GB) has `publicAccessLevel = metadata`, so data access needs approval.
  - Its Redivis record was created on 2026-01-27 (UTC).
- Redivis tokens are created under "Workspace -> Settings -> API tokens". They are long-lived and scoped, for example `data.data`. They are passed as `Authorization: Bearer` or through the `REDIVIS_API_TOKEN` environment variable. OAuth tokens without a client ID last 16 hours — [Redivis authorization](https://docs.redivis.com/api/rest-api/authorization).
- Access levels are "Overview", "Metadata" ("view variable names and summary statistics"), "Sample" and "Data". With data access, users "can view and query all tables and files". Organization-owned datasets are approved "by any administrator of that organization" — [Redivis access levels](https://docs.redivis.com/reference/data-access/access-levels).
- Access can also be gated by "Requirements": users "must complete and be approved for all requirements for an access level" — [Redivis configuring access](https://docs.redivis.com/reference/data-access/configuring-access).
- For many files, `Table.download_files` and `directory.download` download in parallel (search summary) — [Redivis Python directory.download](https://docs.redivis.com/api/client-libraries/redivis-python/reference/directory/directory.download).

#### Synapse
- Downloads use `synapse get <synID>`, `synapse get -r <synID>` for folders, or `synapseutils.syncFromSynapse` in Python, which skips files already downloaded. The cache checks MD5 — [Synapse programmatic download](https://docs.synapse.org/docs/Downloading-Data-Programmatically.2003796248.html).
- "Setting the SYNAPSE_AUTH_TOKEN environment variable will allow you to login to Synapse with a Personal Access Token". It takes priority over `.synapseConfig`, and the token needs at least the view scope; the Download scope is recommended — [synapseclient authentication](https://python-docs.synapse.org/en/stable/tutorials/authentication/).
- "Anonymous users cannot create projects in Synapse, upload or download data." Registered users "can also download publicly available data" — [Synapse account types](https://docs.synapse.org/synapse-docs/synapse-user-account-types).

#### IEEE DataPort
- "You must be an IEEE DataPort subscriber" to get AWS keys from the Account page. The download is `aws s3 cp s3://ieee-dataport/<your-path>/<your-file-name> .` — [IEEE DataPort via AWS](https://ieee-dataport.org/help/accessing-ieee-dataport-dataset-files-through-amazon-web-services-aws).
- Open Access datasets need a free IEEE login. Society members get a free individual subscription (search summary) — [IEEE DataPort FAQ](https://ieee-dataport.org/faq/how-do-i-access-dataset-ieee-dataport).

#### Science Data Bank (scidb.cn)
- Metadata is harvested over OAI-PMH at https://www.scidb.cn/oai. The API status is listed as "uncertain" (registry) — [COAR registry entry](https://ird.coar-repositories.org/systems/b4fe6f36-faa3-474a-9526-e921026c3808?lang=en).
- Login is through a China Academy of Sciences email, CSTCloud, GitHub, ORCID or WeChat. Depositors can set "data acquisition conditions" (search summary of a journal guide) — [JCST guide](https://jcst.ict.ac.cn/supplement/preview/ed976637-decb-439a-832b-6b65bcfbc27f).

#### Harvard Dataverse
- One file comes from `/api/access/datafile/$id`; a whole dataset comes as a zip from `/api/access/dataset/:persistentId/`, and "The Dataverse installation has limited how large the zip bundle can be". "Files that require a Guestbook Response will require an additional step": a POST that "can return a signed url". The token goes in the `X-Dataverse-key` header. The guide is for v6.12.1 — [Dataverse Data Access API](https://guides.dataverse.org/en/latest/api/dataaccess.html).
- Observed: `https://dataverse.harvard.edu/api/info/version` returned `{"version":"6.12.1"}` with HTTP 200 — [Harvard Dataverse API](https://dataverse.harvard.edu/api/info/version).

#### Dryad
- Tokens come from a `client_credentials` grant (`POST https://datadryad.org/oauth/token`) and "Currently our tokens last 10 hours" — [Dryad API accounts](https://github.com/CDL-Dryad/dryad-app/blob/main/documentation/apis/api_accounts.md).
- Observed: `https://datadryad.org/api/v2` returned JSON with HTTP 200 — [Dryad API v2](https://datadryad.org/api/v2).

#### OSF
- The API works without a token, but "authentication ... will increase your rate limit" (search summaries) — [OSF cookbook](https://ua-libraries-research-data-services.github.io/UALIB_ScholarlyAPI_Cookbook/python/osf.html), [osfr auth](https://packages.ropensci.org/osfr/doc/auth.html).
- Observed: `https://api.osf.io/v2/` returned HTTP 200 with no rate-limit headers — [OSF API](https://api.osf.io/v2/).

#### Academic Torrents
- The docs recommend Transmission and list a "Python at-python library", "Backup URLs (WebSeeds)" and a "Legal" section. I could read only the headings — [Academic Torrents docs](https://academictorrents.com/docs/about.html).

#### CREATIS (CAMUS)
- The challenge page links the dataset to the Girder database at humanheart-project.creatis.insa-lyon.fr — [CAMUS challenge page](https://www.creatis.insa-lyon.fr/Challenge/camus/).
- Observed on 2026-11-25: the Girder REST API returned the collection metadata with no login. The values were name "CAMUS_public", `public: true`, size 3,833,335,494 bytes (3.83 GB) and creation date 2022-11-15 — [Girder collection JSON](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection/6373703d73e9f0047faa1bc8).
- The old challenge flow needed an account on the evaluation website ("The challenge is now close") — [CAMUS participation](https://www.creatis.insa-lyon.fr/Challenge/camus/participation.html).

#### Giving a token to a server: what the hosts' docs say
- Zenodo: the header is preferred, and the URL parameter "less secure" — [Zenodo developers](https://developers.zenodo.org/).
- figshare: the header is preferred over `?access_token=` — [figshare API docs](https://docs.figshare.com/).
- Dataverse: the `X-Dataverse-key` header is the "newer" option compared with `key=` — [Dataverse Data Access API](https://guides.dataverse.org/en/latest/api/dataaccess.html).
- Redivis: store the token "in a secure place". Tokens work like passwords, so do not share or commit them, limit scopes, and revoke a token if it may be compromised. The value is shown only once — [Redivis authorization](https://docs.redivis.com/api/rest-api/authorization).
- Synapse: an environment variable overrides the config file, and the minimum scope is view — [synapseclient authentication](https://python-docs.synapse.org/en/stable/tutorials/authentication/).
- Kaggle: the `KAGGLE_API_TOKEN` environment variable or the `~/.kaggle/access_token` file — [Kaggle API docs](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md).

### Inferences
- A download plan can treat most open repositories as HTTPS GETs against an API that lists files with sizes and, for Zenodo and figshare, md5 checksums. The plan only needs a per-host step that lists the files.
- Stanford AIMI datasets are no longer fetched from Azure with a SAS URL and azcopy, at least for the seven ultrasound or echo datasets I saw on Redivis. The plan should use Redivis, with a token from an approved account. Whether the old Azure links still work is unknown.
- For TCIA, TDR is the tool to plan around. It has a CLI and MD5 checks, and its `.s5cmd` manifest input suggests it can fetch from IDC buckets. That last point is inferred from the input format and not confirmed.
- How to handle tokens on EC2, in my reading of the docs above:
  - Keep tokens out of URLs, because URLs end up in logs.
  - Inject tokens at run time as environment variables (`HF_TOKEN`, `KAGGLE_API_TOKEN`, `SYNAPSE_AUTH_TOKEN`, `REDIVIS_API_TOKEN`), taken from the project's own AWS secret route, which these notes do not cover.
  - Use the narrowest scope a host offers (Synapse view and download, Redivis `data.data`).
  - Treat browser cookies (gdown, BaiduPCS-Go) as full account credentials.
- Dryad tokens expire after 10 hours. An unattended job needs the API client secret on the server so it can renew the token. That raises the stakes of storing it.

### Gaps
- Mendeley Data: the official file-download endpoint and whether the public API needs a token. The docs page is a JavaScript app I could not read.
- Science Data Bank: an official batch-download or API reference.
- OneDrive personal accounts, as opposed to Business: whether anonymous API access exists.
- Dropbox: the `dl=1` behaviour.
- GitHub: limits on release-asset downloads.
- Kaggle: phone verification, which has forum evidence only.
- The PhysioNet credentialed `wget --user` form, which is hidden when logged out.
- How Redivis presents the AIMI research use agreement and how long approval takes.
- The lifetime of the old AIMI Azure SAS links. That portal appears replaced.
- Exact Girder download commands for CAMUS (for example `girder-client`), which I did not read.

## 2. Downloads from AWS addresses: blocks, throttling, captchas, quotas, rate limits, resumable downloads, checksums and speeds

### Takeaway
I found no host that documents a block on AWS addresses, and I made no test from EC2. The documented risks are different:
- Per-IP limits for anonymous users (Hugging Face, GitHub, Zenodo, Dryad).
- Per-file and per-owner quotas (Google Drive, Dropbox, GitHub LFS).
- Bot filters in front of web pages. figshare showed an AWS WAF challenge to curl, Grand Challenge refused one fetcher, and Harvard's support site returned 403. In all three cases the API or file endpoint answered normally.

Checksums are offered by Zenodo, figshare, PhysioNet, Synapse, TCIA/TDR, Hugging Face and the cloud drives through rclone. Almost no host reports download speeds.

### Cited Findings

Table 2. Documented rate limits, resume support and checksums per host. "n/f" means not found in the sources I read.

| Host | Documented limit | Resume / HTTP Range | Checksum offered |
|---|---|---|---|
| Zenodo | 60 req/min and 2,000 req/h (guest); 100/min and 5,000/h (token); search 30/min | n/f | md5 per file |
| figshare | no automatic limit; "no more than one request per second" asked | Range headers exposed (observed, untested) | `computed_md5`, `supplied_md5` |
| Hugging Face | per 5 min: anonymous per IP 500 API / 3,000 file / 100 pages; free user 1,000 / 5,000 / 200 | n/f | SHA256 for LFS/Xet files |
| GitHub | 60 req/h unauthenticated per IP; 5,000 req/h with PAT; LFS 10 GiB/month free bandwidth (owner's) | n/f | n/f |
| Google Drive | per-file "high view or download volume" block, about 24 h; 10 TiB/day download per account (rclone) | API Range supported; gdown `--continue` | md5, sha1, sha256 (rclone) |
| Dropbox | link owner: 20 GB/day (Basic) to 1 TB/day (Plus and up) to 4 TB/day | n/f | Dropbox content hash (rclone) |
| Baidu Netdisk | throttling of free accounts | n/f | n/f |
| Dryad | anonymous 30 req/min with a lower limit on file downloads; API account 8 times that | n/f | n/f |
| Harvard Dataverse | separate admin page (not read) | single Range supported | n/f |
| PhysioNet | n/f | `wget -c`, `-N` | `SHA256SUMS.txt` per project |
| TCIA (NBIA/TDR) | n/f | NBIA resumes missing series and retries 4 times; TDR skips existing files | TDR MD5 on by default; NBIA optional |
| Synapse | n/f | sync skips already-downloaded files | MD5 (cache check) |
| Redivis (AIMI) | anonymous caps 1 TB/month per organization and 100 GB/month per user | n/f | n/f |

#### Zenodo
- Documented limits: guests get 60 requests per minute and 2,000 per hour; authenticated users get 100 per minute and 5,000 per hour. Search is limited to 30 per minute and OAI-PMH to 30 per minute. Over the limit, clients get "429 Too Many Requests", and the headers are `X-RateLimit-Limit`, `-Remaining` and `-Reset`. No separate file-download limit is stated — [Zenodo developers](https://developers.zenodo.org/).
- Observed on 2026-11-26 with no token: `x-ratelimit-limit: 133` on the records API. This differs from the documented 60 per minute — [example record API](https://zenodo.org/api/records/1327317).
- New limits since 2025-11-25: "Maximum 30 requests per minute" on records search, and 25 results per page anonymous or 100 authenticated. The reason given is harvesting at "up to 500 requests per second" — [Zenodo blog 2025-11-25](https://blog.zenodo.org/2025/11/25/2025-11-14-search-api-updates/).
- 2026-01-28: automated systems "do not respect our rate limits and actively try to circumvent them". "Basic mitigation techniques such as blocking and rate limiting are no longer sufficient on their own". Zenodo announced new measures "in the coming weeks" but gave no details — [Zenodo blog 2026-01-28](https://blog.zenodo.org/2026/01/28/2026-01-28-improvements-and-support-expectations/).
- A cptac GitHub issue reports HTTP 429 from the single-record endpoint when many parallel HPC jobs ran. This comes from a search summary — [cptac issue 64](https://www.github.com/PayneLab/cptac/issues/64).
- Size: the developer page mentions a newer files API with up to 50 GB per file and 100 files per record — [Zenodo developers](https://developers.zenodo.org/). Grand Challenge cites a "50 GB size limit per repository" — [Grand Challenge data storage](https://grand-challenge.org/documentation/data-storage/).

#### figshare
- "We do not have automatic rate limiting in place for API requests." "We recommend ... do not make more than one request per second." "We reserve the right to throttle or block requests if we detect abuse." — [figshare API docs](https://docs.figshare.com/).
- Observed on 2026-11-25: `https://figshare.com/terms` returned HTTP 202 with `content-length: 0` and `x-amzn-waf-action: challenge`, served by `awselb/2.0`. That is an AWS WAF JavaScript challenge. The API and the ndownloader file endpoint answered normally — [figshare terms URL](https://figshare.com/terms).

#### Hugging Face
- The limits apply per 5-minute fixed window, as of September 2025:
  - Anonymous (per IP address): 500 API, 3,000 resolver (file) and 100 page requests.
  - Free user: 1,000, 5,000 and 200.
  - PRO: 2,500, 12,000 and 400.
  - Team or Academia Hub: 3,000, 20,000 and 400.
  - Over the limit, clients get HTTP 429 with `RateLimit` headers. `huggingface_hub` 1.2.0 and later waits out a 429 automatically — [HF rate limits](https://huggingface.co/docs/hub/rate-limits).
- When downloading, `hf_xet` queries the Xet service "with the LFS SHA256 hash for this file" — [HF download guide](https://huggingface.co/docs/huggingface_hub/guides/download).

#### GitHub
- "The primary rate limit for unauthenticated requests is 60 requests per hour", tied to the originating IP. A PAT gives 5,000 per hour. Secondary limits are 100 concurrent requests and 900 points per minute — [GitHub REST rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api).
- Git LFS bandwidth: "When you download a Git LFS file, the bandwidth you use is included in the repository owner's bandwidth usage." Free plans get 10 GiB each of bandwidth and storage per month; Team and Enterprise Cloud get 250 GiB. Over quota without a payment method, "Git LFS support is disabled on your account until the next month". Prepaid data packs were "replaced with metered billing" — [GitHub LFS storage and bandwidth](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-storage-and-bandwidth-usage).

#### Google Drive
- "This error occurs when a file receives high view or download volume over a short period." "The restriction is temporary and typically resets within 24 hours." The workaround is to copy the file into your own Drive and download the copy. Owners are told to "Use Google Cloud Storage or dedicated hosting solutions for large files" — [Google Drive help](https://support.google.com/drive/answer/2423534?hl=en).
- rclone notes:
  - "it is only possible to download 10 TiB of data from Google Drive a day" and "upload 750 GiB" a day.
  - Each client_id is limited to "about 2 files per second".
  - "If you see User rate limit exceeded errors, wait at least 24 hours".
  - Hashes are MD5, SHA1 and SHA256 — [rclone drive](https://rclone.org/drive/).
- gdown: "Google throttles downloads when too many people access the same file, but lets a signed-in account through." `cached_download` can check an md5 — [gdown README](https://github.com/wkentaro/gdown).

#### Dropbox
- Daily limits on the link owner's account:
  - Basic: "20 GB and up to 100,000 file downloads per day".
  - Plus, Family, Professional, Essentials, Standard and Business: "1 TB and unlimited file downloads per day".
  - Advanced, Business Plus and Enterprise: "4 TB".
  - A first offence pauses sharing "for 24 hours" — [Dropbox banned links](https://help.dropbox.com/share/banned-links).
- An older forum post says 200 GB per day for Pro and Business, which contradicts the help page — [Dropbox forum](https://www.dropboxforum.com/t5/Plans-and-Subscriptions/Banned-links-or-temporarily-disabled-links/m-p/127339).

#### Baidu Netdisk
- BaiduPCS-Go tells regular users to set `max_parallel` and `max_download_load` to 1. More threads "极易很快触发限速" (very easily trigger throttling) and can leave the account near zero speed in every client "几小时至几天" (for hours to days). "本软件不支持普通用户提速" (no speed-up for regular users) — [BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go).
- One seller's forum post measured 53 KB/s on one stream and 71 KB/s on 16 connections with a free account, and 19 MB/s with SVIP (paid). Unverified — [HF forum post](https://discuss.huggingface.co/t/how-to-download-from-baidu-pan-pan-baidu-com-without-a-chinese-account-2026-notes-for-datasets-a-free-fetcher/180125).

#### Dryad
- "Anonymous users of the API are limited to 30 requests per minute, with a lower limit for downloads of data files." An API account gives "8 times the rate of anonymous API users". This comes from a search summary of the official API page — [Dryad API](https://datadryad.org/api).
- A third-party mirror of Dryad's API description says anonymous users "are not allowed to download data files". This conflicts with the official wording above — [apis.io Dryad files API](https://apis.io/apis/dryad/dryad-files-api/).

#### Harvard Dataverse, PhysioNet, TCIA, Synapse, Redivis, Grand Challenge
- Dataverse: Range "Only a single range is supported". Rate limiting is on a separate admin-guide page — [Dataverse Data Access API](https://guides.dataverse.org/en/latest/api/dataaccess.html).
- Observed: Harvard's support site (the terms page) returned HTTP 403 to curl and to WebFetch. The response carried an Akamai `server-timing: ak_p` header. The API itself answered with HTTP 200 — [Harvard Dataverse terms URL](https://support.dataverse.harvard.edu/harvard-dataverse-general-terms-use).
- PhysioNet: the PTB-XL folder lists `SHA256SUMS.txt`, and the wget command uses `-c` (continue) and `-N` (timestamping) — [PhysioNet PTB-XL page](https://physionet.org/content/ptb-xl/1.0.3/).
- TCIA NBIA Data Retriever: after network errors "the app retries automatically", 4 attempts by default. It offers "Download missing series" on restart. Checksum verification is optional; otherwise it checks file sizes — [TCIA download page](https://wiki.cancerimagingarchive.net/display/NBIA/Downloading+TCIA+Images).
- TDR: MD5 on by default (`--no-md5` turns it off), with pause and resume through skip-existing logic — [TDR on GitHub](https://github.com/TCIA/data-retriever).
- Synapse: "the cache is checked to see if the same file is already present by checking its MD5 checksum" — [Synapse programmatic download](https://docs.synapse.org/docs/Downloading-Data-Programmatically.2003796248.html).
- Redivis: "Anonymous API users will also generally experience tighter rate-limiting". Anonymous downloads are capped at 1 TB per month per organization and 100 GB per month per user — [Redivis authorization](https://docs.redivis.com/api/rest-api/authorization).
- Grand Challenge: WebFetch got HTTP 403 on the terms and docs pages. curl with a Firefox user-agent got HTTP 200 (observed 2026-11-25), which suggests user-agent filtering — [Grand Challenge ToS](https://grand-challenge.org/policies/terms-of-service/).

### Inferences
- None of the hosts' documents say they block AWS addresses. Even so, an EC2 address shares and inherits IP-based limits and bot scores, so I would expect more challenges than from machine01. Zenodo's 2026 measures against bots may also reach datacentre traffic. These are inferences with no test behind them.
- The safe pattern is the official API with a token, a descriptive User-Agent, low concurrency (figshare asks for at most 1 request per second) and backoff on HTTP 429. Before a full run, the instance should make one small probe per host.
- Google Drive is the most fragile host. Popular files hit the per-file block. The rclone shared client ID stops working in 2026, so rclone needs our own OAuth client. A copy into our own Drive (the documented workaround) is a manual step.
- Baidu Netdisk at about 50 to 70 KB/s (unverified) would take about 4 to 5 hours per GB. That makes a free account impractical for multi-GB datasets.
- Verification can be planned per host: md5 for Zenodo and figshare, SHA256 sums for PhysioNet, MD5 for TDR and Synapse, SHA256 for Hugging Face. Kaggle, Dropbox links, OneDrive links and Baidu need a checksum of our own after download, or the provider's checksum if published elsewhere.

### Gaps
- I found no measured download speeds from EC2 for any host. The only figures are the unverified Baidu ones.
- I found no primary evidence of Google Drive captchas on datacentre addresses.
- Not found in the sources I read: Range or resume support for Zenodo, Hugging Face, Kaggle and Girder (CAMUS); the rate limits of Kaggle, OSF, Mendeley Data, Science Data Bank and Harvard Dataverse; and Dataverse checksums.

## 3. Can any host send data straight to S3?

### Takeaway
A true server-side copy into our bucket works only from data already in S3: the AWS ODR, IDC buckets, PhysioNet's open bucket and possibly others. `aws s3 cp` or `sync` between buckets copies inside S3, and transfer within us-east-1 is free. Everything else streams through the EC2 instance. That includes IEEE DataPort's bucket (keys from another account), the Azure-hosted data and every HTTP host. Tools such as `rclone copyurl` stream with no local temporary file. azcopy copies only from S3 to Azure, not the other way.

### Cited Findings
- S3 CopyObject: "You must have *read* access to the source object and *write* access to the destination bucket" (`s3:GetObject` and `s3:PutObject`). It copies "up to 5 GB in size in a single atomic action"; larger objects need `UploadPartCopy` — [S3 CopyObject](https://docs.aws.amazon.com/AmazonS3/latest/API/API_CopyObject.html).
- S3 pricing lists free transfer for "Data transferred between S3 buckets in the same AWS Region" and "from an Amazon S3 bucket to any AWS service(s) within the same AWS Region ... (including to a different account in the same AWS Region)" — [S3 pricing](https://aws.amazon.com/s3/pricing/).
- Requester Pays: "anonymous access to that bucket is not allowed". Requesters add `x-amz-request-payer` or `--request-payer` and pay "the cost of the request and the data download" — [S3 Requester Pays](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html).
- These buckets are in us-east-1 with anonymous access:
  - IDC: `idc-open-data`, `idc-open-data-two` and `idc-open-data-cr` — [AWS ODR: IDC](https://registry.opendata.aws/nci-imaging-data-commons/).
  - PhysioNet open data: `s3://physionet-open/...` — [PhysioNet PTB-XL page](https://physionet.org/content/ptb-xl/1.0.3/).
  - `physionet-pds` (us-east-1, "Not updated", marked deprecated) — [AWS ODR: PhysioNet](https://registry.opendata.aws/physionet/).
- Grand Challenge recommends the AWS ODR to challenge organisers for "No size restrictions like Zenodo", "Direct access via AWS S3" and "Free data downloads" — [Grand Challenge data storage](https://grand-challenge.org/documentation/data-storage/).
- IEEE DataPort data sits in S3 bucket `ieee-dataport`, read with subscriber keys. The region is not stated — [IEEE DataPort via AWS](https://ieee-dataport.org/help/accessing-ieee-dataport-dataset-files-through-amazon-web-services-aws).
- Synapse stores files by default in "Synapse-managed S3 storage". Projects can also point at their own buckets. The region was not confirmed (search summary) — [Synapse custom storage locations](https://docs.synapse.org/synapse-docs/custom-storage-locations), [synapseclient storage architecture](https://python-docs.synapse.org/explanations/storage_location_architecture/).
- rclone `copyurl` will "Download a URL's content and copy it to the destination without saving it in temporary storage", with `--auto-filename` and `--header-filename` — [rclone copyurl](https://rclone.org/commands/rclone_copyurl/).
- When a server cannot copy directly, "the file is downloaded then re-uploaded" — [rclone overview](https://rclone.org/overview/).
- rclone `azureblob` accepts a `sas_url`, where "a container level SAS URL" limits it to that container. Public anonymous containers need only `account` (`:azureblob,account=ACCOUNT:CONTAINER`) — [rclone azureblob](https://rclone.org/azureblob/).
- AzCopy documents copying "from Amazon Web Services (AWS) S3 to Azure Blob Storage" with Put Block From URL, so "data is copied directly between AWS S3 and storage servers" — [AzCopy from S3](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-s3).
- Redivis export environments can restrict exports "to a specific IP address, BigQuery project, Cloud Storage bucket"; downloads need data access and must not conflict with the dataset's export restrictions (search summary) — [Redivis usage rules](https://docs.redivis.com/reference/data-access/usage-rules), [Redivis export environments](https://docs.redivis.com/reference/organizations/settings/export-environments).

### Inferences
- From the AWS ODR, IDC or PhysioNet open buckets, run `aws s3 sync s3://<public-bucket>/<prefix> s3://<our-bucket>/<prefix>` with our own credentials. That copies inside S3, at no transfer cost within us-east-1.
  - This works only if the source bucket policy also lets authenticated principals read. A typical public policy with principal `*` does, but that is my inference; check it per bucket.
  - Objects over 5 GB use multipart copy, which the CLI handles. That part is unverified.
- IEEE DataPort: subscriber keys belong to IEEE's account, not ours, so one CopyObject cannot read their bucket and write ours. The copy must stream through EC2, for example `aws s3 cp s3://ieee-dataport/... -` piped to `aws s3 cp - s3://<ours>/...` under two profiles. This is inference.
- HTTP hosts (Zenodo, figshare, Dataverse, Dryad, OSF, PhysioNet open, CAMUS Girder, Mendeley Data, lab sites): `rclone copyurl <url> <s3 remote>:<bucket>/<key>` or `curl ... | aws s3 cp - s3://...` streams through the instance with no local disk. Uploads to S3 in the same region are free. The checksum must then be checked separately, because the HTTP backend has no hash.
- Azure-hosted data with a SAS URL, if any remains: `rclone copy :azureblob,sas_url=...: s3remote:bucket` streams through the rclone host. azcopy cannot write to S3, per its documentation.
- Redivis (AIMI): no S3 export destination is documented, so data goes through the Redivis client on the instance. Some datasets may also need admin approval for each export destination.

### Gaps
- The regions of the Synapse default storage and of the IEEE DataPort bucket, and whether Synapse pre-signed download URLs point at us-east-1.
- Whether Redivis can export to S3.
- Whether the IDC and PhysioNet bucket policies allow authenticated cross-account reads. Anonymous reads are documented.

## 4. What the hosts' terms of service say about automated or bulk downloading

### Takeaway
Few terms address automated downloading directly. The general rule across them is that the documented API or official tools are fine, while scraping web pages, evading limits and excessive bulk traffic are not. The terms that prohibit something are Kaggle (crawling and storing "any significant portion"), figshare (robots, per institutional copies of its terms), Dropbox and Google (only public interfaces; respect robots.txt), GitHub (excessive bulk activity, with a research exception for scraping) and Grand Challenge (no bot accounts). Zenodo and Hugging Face rely on rate limits instead of ToS clauses.

### Cited Findings
- Zenodo: the ToS has no automation clause. "CERN reserves the right ... to restrict or remove User access where it considers that use of Zenodo interferes with its operations". "Users of content ("Users") shall respect applicable license conditions." — [Zenodo terms](https://about.zenodo.org/terms/).
- figshare: institutional copies of figshare's terms bar using "any manual or automated means, such as robots, scripts, or spiders, to crawl, scrape, or mine" without written authorisation. This comes from a search summary; the live page is behind a WAF challenge — [Chapman copy of figshare terms](https://www.chapman.edu/library/_files/documents/chapman-figshare-terms.pdf), [Oxford SDS terms](https://sds.web.ox.ac.uk/terms-use).
- Kaggle (search snippets of the JavaScript-only terms pages):
  - The ToS prohibits anyone who "Crawls," "scrapes," or "spiders" any page, data, or portion of or relating to the Services or Content (through use of manual or automated means), and also copying or storing any significant portion of the content — [Kaggle terms](https://www.kaggle.com/terms).
  - The AUP lists "excessive crawling" — [Kaggle AUP](https://www.kaggle.com/aup).
  - A Kaggle staff member said in 2016 that one developer's crawling API was "fine", which is informal — [Kaggle forum](https://www.kaggle.com/discussions/general/22832).
- Hugging Face: the ToS has no automation clause. When content "contains notice of a reasonable and customary license, such Content is intended to remain under the terms of such license". Third-party content is "subject to these Terms and/or the terms accompanying such Content" — [HF terms of service](https://huggingface.co/terms-of-service).
- GitHub:
  - "Scraping does not refer to the collection of information through our API."
  - "Researchers may use public, non-personal information from the Service for research purposes, only if any publications resulting from that research are open access."
  - Prohibits "excessive automated bulk activity".
  - Excessive bandwidth may lead GitHub to "throttle your file hosting" — [GitHub acceptable use](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies).
- Google: prohibits "using automated means to access content from any of our services in violation of the machine-readable instructions on our web pages (for example, robots.txt files that disallow crawling, training, or other activities)" — [Google terms](https://policies.google.com/terms?hl=en).
- Dropbox: prohibits "access, search, or create accounts for the Services by any means other than our publicly supported interfaces (for example, "scraping" or creating accounts in bulk)" — [Dropbox acceptable use](https://www.dropbox.com/acceptable_use).
- Grand Challenge: "Accounts registered by "bots" or other automated methods are not permitted." "Your login may only be used by one person". Use of the API is "bound by these Terms of Service plus the following specific terms" — [Grand Challenge ToS](https://grand-challenge.org/policies/terms-of-service/).
- Synapse (Sage Bionetworks terms): "Maintain your account security and not share your account credentials." General content is "subject to any Content specific restrictions, e.g., user training, controlled access, limited use, Content redistribution limitations" — [Sage terms](https://github.com/Sage-Bionetworks/Sage-Governance-Documents/blob/master/Terms.md).
- TCIA: anyone "mirroring" datasets or giving access through another tool must follow the Data Analysis Centers requirements. They must attribute each dataset, link the usage policy and require the same of downstream users — [TCIA data usage policy](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/).
- Zenodo's 2025 and 2026 blog posts (Q2) describe bulk harvesting of search as the problem and point bulk metadata users to OAI-PMH and monthly dumps — [Zenodo blog 2025-11-25](https://blog.zenodo.org/2025/11/25/2025-11-14-search-api-updates/).

### Inferences
- My reading: a plan that fetches specific datasets through each host's API or official CLI, at modest concurrency, with a token where offered, fits all the clauses above. Scraping Kaggle or figshare web pages or rotating IP addresses would not.
- GitHub's research exception covers scraping. Plain git clone or API use is not scraping under its own definition.
- Kaggle's "storing any significant portion" clause is about the site's content in general. Dataset downloads through the official API are the sanctioned route, but the licence and the competition rules (Q5) still govern use. This is my reading.

### Gaps
- I could not read these terms: Mendeley Data (JavaScript page), Harvard Dataverse (403), figshare live terms (WAF), OSF, Dryad, Science Data Bank, IEEE DataPort, Academic Torrents ("Legal" section not readable), Microsoft Services Agreement (OneDrive/SharePoint) and Baidu.
- I did not check the AWS acceptable use policy for BitTorrent on EC2.

## 5. The main data use agreements and challenge terms: (a) private copy in our own cloud bucket, (b) training models, commercial or not, (c) sharing inside a small team, (d) attribution, (e) deletion at end of use, (f) re-identification

### Takeaway
My reading, not legal advice:
- The strict agreements are the PhysioNet credentialed DUA, the Stanford AIMI RUA and the NIH DUC that now governs restricted TCIA data. All three bind individuals: no shared access, so every team member applies or signs, and each forbids re-identification.
- Stanford AIMI allows only "personal, non-commercial research". Commercial use needs a paid licence ($70,000 per dataset per year in fiscal year 2025).
- PhysioNet allows "scientific research and no other", and PhysioNet states that sending its data through third-party APIs violates the DUA.
- The NIH DUC requires declaring the cloud provider and destroying all copies at project close.
- TCIA open data is mostly CC BY, so commercial use is allowed.
- Kaggle, Grand Challenge, Synapse and Hugging Face gated data are governed by terms set per competition or per dataset. CAMUS looks non-commercial (CC BY-NC-SA per a mirror), with citation required.

### Cited Findings

#### Stanford AIMI research use agreement (EchoNet-Dynamic text)
The text below is the EchoNet-Dynamic RUA as published on the dataset's own site — [EchoNet-Dynamic RUA](https://echonet.github.io/dynamic/).
- Scope: "By registering for downloads from the EchoNet-Dynamic Dataset, you are agreeing to this Research Use Agreement, as well as to the Terms of Use of the Stanford University School of Medicine website".
- Clause 1: "Permission is granted to view and use the EchoNet-Dynamic Dataset without charge for personal, non-commercial research purposes only. Any commercial use, sale, or other monetization is prohibited."
- Clause 3: "You may make a verbatim copy of the EchoNet-Dynamic Dataset for personal, non-commercial research use as permitted in this Research Use Agreement. If another user within your organization wishes to use the EchoNet-Dynamic Dataset, they must register as an individual user and comply with all the terms of this Research Use Agreement."
- Clause 4: "YOU MAY NOT DISTRIBUTE, PUBLISH, OR REPRODUCE A COPY of any portion or all of the EchoNet-Dynamic Dataset to others without specific prior written permission from the School of Medicine."
- Clause 5: "YOU MAY NOT SHARE THE DOWNLOAD LINK to the EchoNet-Dynamic dataset to others."
- Clause 6: "You must not modify, reverse engineer, decompile, or create derivative works from the EchoNet-Dynamic Dataset."
- Clause 7: "for non-clinical, Research Use Only".
- Clause 9: "You will not make any attempt to re-identify any of the individual data subjects. Re-identification of individuals is strictly prohibited. Any re-identification of any individual data subject shall be immediately reported to the School of Medicine."
- Clause 10: on a violation, the School "may direct that the undersigned data recipient immediately return all copies of the EchoNet-Dynamic Dataset and retain no copies thereof".
- Other AIMI agreements differ:
  - EchoNet-Pediatric's says "You may not otherwise copy, reproduce, retransmit, distribute, publish, commercially exploit or otherwise transfer any material" (search summary) — [EchoNet-Pediatric](https://echonet.github.io/pediatric).
  - The LERA dataset agreement uses the same "personal, non-commercial research purposes only" clause (search summary) — [AIMI LERA](https://aimi.stanford.edu/datasets/lera-lower-extremity-radiographs).
- Attribution: users "are expected to acknowledge Stanford AIMI in publications and presentations" with given wording, starting "This research used data provided by the Stanford Center for Artificial Intelligence in Medicine and Imaging (AIMI)..." — [AIMI shared datasets](https://aimi.stanford.edu/shared-datasets). The dataset page asks for the DOI https://doi.org/10.71718/yqp5-y078 — [AIMI EchoNet-Dynamic](https://aimi.stanford.edu/datasets/echonet-dynamic-cardiac-ultrasound).
- Commercial: the datasets are "shared broadly under a license that is restricted to non-commercial purposes". "The annual fee is $70,000 USD per dataset for agreements contracted in FY25 (through 8/31/25)", with a one-year term, committee review and no discounts — [AIMI commercial use](https://aimi.stanford.edu/datasets-commercial-use).

#### PhysioNet Credentialed Health Data License 1.5.0 (credentialed DUA)
The clauses below are quoted verbatim from the licence — [PhysioNet licence 1.5.0](https://physionet.org/about/licenses/physionet-credentialed-health-data-license-150/).
- 1: "The LICENSEE will not attempt to identify any individual or institution referenced in PhysioNet restricted data."
- 2: "...exercise all reasonable and prudent care to avoid disclosure of the identity of any individual or institution ... in any publication or other communication."
- 3: "The LICENSEE will not share access to PhysioNet restricted data with anyone else."
- 4: "...exercise all reasonable and prudent care to maintain the physical and electronic security of PhysioNet restricted data."
- 5: report possibly identifying information "promptly by email to PHI-report@physionet.org".
- 6: "The LICENSEE will use the data for the sole purpose of lawful use in scientific research and no other."
- 7: keep "up to date certification in human research subject protection and HIPAA regulations".
- 8: "contribute code associated with publications arising from this data to a repository that is open to the research community".
- 9: "This agreement may be terminated by either party at any time, but the LICENSEE's obligations with respect to PhysioNet data shall continue after termination."
- Online services: "The PhysioNet Credentialed Data Use Agreement explicitly prohibits sharing access to the data with third parties, including sending it through APIs provided by companies like OpenAI, or using it in online platforms like ChatGPT." PhysioNet suggests Azure OpenAI with human review opted out, Amazon Bedrock or Google's Gemini instead (2023-04-18) — [PhysioNet note](https://physionet.org/news/post/gpt-responsible-use).
- Citation: each project page asks users to cite the dataset and "include the standard citation for PhysioNet" — [MIMIC-IV-ECHO page](https://physionet.org/content/mimic-iv-echo/0.1/).

#### TCIA data usage policy, and the restricted-collection route
- "Most data are freely available to browse, download, and use for commercial, scientific and educational purposes" under CC BY 3.0 or CC BY 4.0. "A small number of collections" restrict commercial use, and "this is no longer an option for new submissions" — [TCIA data usage policy](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/).
- Citation: "Every TCIA dataset is published with a Data Citation", which "must be cited or attributed any time the data are used" — [TCIA data usage policy](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/).
- Re-identification: users must not use the data "alone or combined with other information" to identify or contact participants, and must not generate information such as facial images in a way that could reveal identity. IRB-approved research under 45 CFR 46 is exempt. This is a summary of the policy page — [TCIA data usage policy](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/).
- Restricted collections: after the NIH policy change in April 2025, datasets that need data use agreements are hosted with the CRDC, and dbGaP handles access requests — [TCIA data usage policy](https://www.cancerimagingarchive.net/data-usage-policies-and-restrictions/), [TCIA legal framework](https://wiki.cancerimagingarchive.net/display/Public/LEGAL+FRAMEWORK+AND+ETHICAL+USE+OF+THIS+RESOURCE).
- An unofficial note dates the end of TCIA hosting of controlled-access data to 2025-07-08 — [hackmd note](https://hackmd.io/@kirbyju/rySz6il-zl).
- NIH data use certification (version of 2023-12-20), read as text from the PDF — [NIH Universal DUC](https://sharing.nih.gov/sites/default/files/flmngr/Universal_DUC.pdf):
  - Cloud: investigators "must request permission to use Cloud Computing in the DAR and identify the Cloud Service Provider (CSP)" and submit "a Cloud Computing Use Statement".
  - Team: collaborators at an external site "must submit an independent DAR". Access is granted "for a period of one (1) year, with the option to renew".
  - Term 13: "Upon Project Close-out, the Requester and Approved Users agree to destroy all copies, versions, and Data Derivatives of the dataset(s) ... and if cloud computing was used, delete the data and cloud images from cloud computing provider storage".
- New and renewed DUCs include the NIH Security Best Practices from 2025-01-25 (search summary) — [NIH security best practices](https://sharing.nih.gov/node/208).

#### Kaggle competition rules (typical text; each competition picks its own)
These come from search-engine renderings of kaggle.com rules pages, which are JavaScript-only, so I could not fetch them — [BirdCLEF+ 2025 rules](https://www.kaggle.com/competitions/birdclef-2025/rules), [Products-10K rules](https://www.kaggle.com/competitions/products-10k/rules).
- Hosts choose one of three data tiers: "Competition Use only", non-commercial and academic research, or any commercial or non-commercial purpose.
- Typical non-commercial wording: you may use the data "for non-commercial purposes only, including for participating in the Competition and on Kaggle.com forums, and for academic research and education".
- Some competitions add a licence, for example "CC-BY-NC 4.0" or CC BY-NC-SA, and the Rules "will govern ... if the license conflicts".
- Participants "agree not to transmit, duplicate, publish, redistribute or otherwise provide or make available the Competition Data to any party not participating in the Competition".
- The sponsor "may disqualify any participant who uses the Competition Data other than as permitted".
- Kaggle says it "is not able to approve individual uses of data on a case-by-case basis" (search summary) — [Kaggle forum](https://www.kaggle.com/general/9893).

#### Grand Challenge (platform terms and challenge rules)
- Platform definition: "Research Use Only : Use that is solely for scientific or academic purposes and expressly excludes any clinical, diagnostic, therapeutic, or regulatory use." On tools: "Unless otherwise stated, access to such tools is licensed for research purposes only and not for clinical or commercial use." — [Grand Challenge ToS](https://grand-challenge.org/policies/terms-of-service/).
- Uploaded data must be "fully anonymized in accordance with Regulation (EU) 2016/679 (GDPR)" — [Grand Challenge ToS](https://grand-challenge.org/policies/terms-of-service/).
- Data rules are set per challenge (search summaries):
  - CHAIMELEON grants a non-commercial, revocable licence for the challenge only, with no distribution — [CHAIMELEON terms](https://chaimeleon.grand-challenge.org/terms-conditions/).
  - Thompson lets participants "use the training data in any way they wish for training the models" — [Thompson policy](https://thompson-challenge.grand-challenge.org/participation-policy/).
  - WSSS4LUAD is CC BY 4.0 — [WSSS4LUAD licence](https://wsss4luad.grand-challenge.org/License/).

#### Synapse (Sage terms and conditions for use)
- From the Sage terms — [Sage terms](https://github.com/Sage-Bionetworks/Sage-Governance-Documents/blob/master/Terms.md):
  - "Respect the intellectual property rights of others and acknowledge contributors in all presentations."
  - "Not discriminate, identify, or re-contact individuals or groups represented by the Data."
  - "Maintain your account security and not share your account credentials."
  - Content is subject to "Content specific restrictions, e.g., user training, controlled access, limited use, Content redistribution limitations, as determined by the Content contributor".
- Users must qualify under both the sharing settings and the conditions for use — [Synapse data access types](https://docs.synapse.org/synapse-docs/data-access-types).
- Each person accepts the conditions individually, and sharing one account is prohibited (search summary of a docs mirror) — [Synapse docs mirror](https://kdaily.github.io/synapseDocs/articles/contribute_and_access_controlled_use_data.html).
- One portal's data use certificate was revised for "NIH guidance on AI tool use and NIST 800-171 environments" (search summary) — [AD Knowledge Portal](https://help.adknowledgeportal.org/apd/requesting-access).

#### CAMUS (CREATIS)
- "You must cite this paper for any use of the CAMUS database": Leclerc et al., IEEE TMI 38(9):2198-2210, 2019, doi:10.1109/TMI.2019.2900516 — [CAMUS databases page](https://www.creatis.insa-lyon.fr/Challenge/camus/databases.html).
- No licence text appears on the CREATIS pages I read — [CAMUS challenge page](https://www.creatis.insa-lyon.fr/Challenge/camus/).
- The Academic Torrents mirror lists "CC BY-NC-SA 4.0" and "strictly only non-commercial scientific research purposes". This is a secondary source, seen in a search summary — [Academic Torrents CAMUS](https://academictorrents.com/details/ae545c1e3ce045c33942f89e67f618a6439104a6).

#### Hugging Face gated datasets
- Authors choose automatic or manual approval and may add form fields; the docs example adds a checkbox "I agree to use this dataset for non-commercial use ONLY".
- "Access requests are always granted to individual users rather than to entire organizations."
- Authors "can decide at any time to block your access to the dataset without prior notice" — [HF gated datasets](https://huggingface.co/docs/hub/datasets-gated).
- The licence notice on the repository keeps governing the content — [HF terms of service](https://huggingface.co/terms-of-service).

Table 3. My reading (not legal advice) of each agreement on six points: (a) a private copy in our own cloud bucket, (b) training models, (c) sharing inside a small team, (d) attribution, (e) deletion at the end of use, (f) re-identification. Quotes and sources are in the bullets above. "NC" means non-commercial.

| Agreement | (a) private cloud copy | (b) training; NC vs commercial | (c) small team | (d) attribution | (e) deletion at end | (f) re-identification |
|---|---|---|---|---|---|---|
| Stanford AIMI RUA (EchoNet-Dynamic) | a "verbatim copy" for the registered person's own NC research; a shared bucket only if every user registers | NC research only; clause 6 bars "derivative works", and whether a model is one is unclear; commercial needs the paid licence | each person registers; no link sharing, no copies to others | AIMI wording plus the dataset DOI | none at end; return all copies on violation | forbidden; report any |
| PhysioNet credentialed DUA 1.5.0 | allowed with "physical and electronic security" (not explicit); no third-party APIs | "scientific research and no other"; commercial product use not covered, so ask PhysioNet | each person credentialed and signs | per project page, plus PhysioNet citation; share code from publications | no deletion clause; duties outlive termination | forbidden; report any |
| TCIA open (CC BY) | allowed | allowed, commercial included, except legacy NC collections | allowed | Data Citation DOI | none | forbidden (policy) |
| TCIA restricted via dbGaP (NIH DUC) | only with the cloud provider named in the approved DAR | only the approved research use | named users only; outside sites file their own DAR | not extracted (gap) | destroy all copies, cloud included, at close-out | not extracted (gap) |
| Kaggle competition rules | not addressed; copy only for participants | depends on the tier: competition only, NC research, or commercial | only to participants, so each member accepts the rules | not found (gap) | not found (gap) | not found (gap) |
| Grand Challenge | per challenge | platform: research only, no clinical use; data terms per challenge (NC to "any way") | one login per person; data per challenge | per challenge | none for downloaded data | per challenge; uploads must be anonymised |
| Synapse | per conditions for use | per conditions for use | each person accepts; no shared accounts | "acknowledge contributors" | per conditions | "Not ... identify, or re-contact" |
| CAMUS | allowed for NC if CC BY-NC-SA applies | NC only; share-alike may reach adapted material | allowed for NC | cite the 2019 TMI paper | none found | none found |
| Hugging Face gated | per dataset terms | per dataset terms (gate may require NC) | access per individual; each member requests | per dataset | per dataset | per dataset |

### Inferences
- Commercial case. In my reading the following exclude commercial use as written: Stanford AIMI datasets without the paid licence, PhysioNet credentialed data (beyond "scientific research"), CAMUS (if CC BY-NC-SA), NC-tier Kaggle competitions and NC Grand Challenge data. TCIA CC BY collections and permissively licensed repository data stay usable. The project should settle whether its use is commercial before relying on any NC source.
- Non-commercial case. Training models is plausible under every agreement here. AIMI's clause 6 ("derivative works") and CAMUS's share-alike clause raise the open question of whether a trained model is an adaptation. I cannot settle that; a lawyer or the provider should.
- Team sharing. AIMI, PhysioNet, the NIH DUC, Synapse, Grand Challenge (one login per person) and Hugging Face gating all bind individuals. One bucket shared by the team is consistent with them only if every person who can read it holds their own approval. In my reading, a shared copy for people without access breaks AIMI clauses 3 to 5 and PhysioNet clause 3.
- Project-specific flags for the user, not decided here:
  - (1) PhysioNet's note says sending credentialed data through third-party APIs breaks the DUA. In my reading, an agent session must not read credentialed PhysioNet text or tables into the conversation. [DEC-052](../../decisions/DEC-052-privacy-covers-images-tables-readable-after-asking.md) (images are patient data; tables may reach Anthropic's API) accepts tables reaching the API for project data, which would conflict for credentialed data.
  - (2) Restricted TCIA data in S3 needs the cloud provider named in the DAR.
  - (3) How [DEC-024](../../decisions/DEC-024-plain-never-leaves-machine01-ec2-label-studio-decrypts-in-ram.md) (plain-style data never leaves machine01) and DEC-052 apply to public images fetched straight onto EC2 is for the project to decide.

### Gaps
- The exact text of the AIMI agreement as presented on Redivis. I quote the EchoNet-Dynamic text from the dataset's own site.
- The NIH DUC clauses on re-identification and acknowledgement, which I did not extract.
- The old TCIA Restricted License Agreement text, now replaced by dbGaP.
- The full live text of Kaggle rules, which are JavaScript-only. I used search snippets.
- A primary licence statement for CAMUS from CREATIS. The only licence source is a mirror.
- Per-dataset conditions on Synapse and Hugging Face, which are left to the dataset-level researchers.

## 6. Tools and their fit; one-time manual steps for the user and how long they take

### Takeaway
A small kit covers almost every host:
- aria2c for plain HTTP, URL lists and torrents.
- rclone for the cloud drives, Azure SAS, S3 and `copyurl` streaming.
- Each host's official client where a login is involved: kaggle, hf, synapseclient, TDR or tcia_utils, the Redivis client, gcapi, and wget or the physionet package.
- zenodo_get or datahugger as a convenience for DOI-based repositories.
- BaiduPCS-Go only as a last resort.

The manual steps that take longest are PhysioNet credentialing (typically 1 to 2 weeks; significant delays announced in June 2026), dbGaP approval for restricted TCIA data (no figure found) and Stanford AIMI approval on Redivis (no figure found).

### Cited Findings

Table 4. Download tools and where they fit. Sources are in the bullets below the table.

| Tool | Hosts | Auth handling | Resume | Checksum |
|---|---|---|---|---|
| aria2c | any HTTP(S), FTP, SFTP, BitTorrent, Metalink | `--header` (for example a bearer token), `--load-cookies` | `-c` | `--checksum`, per-URI `checksum=` in `-i` lists |
| rclone | S3, Azure Blob (SAS), Google Drive, OneDrive, Dropbox, HTTP, WebDAV, SFTP and more | per-backend OAuth or keys; `sas_url` | re-runs skip existing files (copy/sync) | per backend (table in rclone overview) |
| gdown | Google Drive public files and folders | cookies file or `--cookies-from-browser` | `--continue` | md5 via `cached_download` |
| kaggle CLI | Kaggle datasets and competitions | `KAGGLE_API_TOKEN`, `access_token`, `kaggle.json`, OAuth login | n/f | n/f |
| hf CLI / huggingface_hub (hf_xet) | Hugging Face | `HF_TOKEN` | local cache skips up-to-date files | SHA256 (LFS/Xet) |
| zenodo_get | Zenodo | n/f | n/f | md5 list `-m` |
| datahugger | DOI-based repositories (Zenodo, Dataverse, figshare, Dryad, OSF, Mendeley Data and more) | n/f | n/f | n/f |
| synapseclient | Synapse | `SYNAPSE_AUTH_TOKEN` | sync skips existing | MD5 |
| TDR, tcia_utils v4, NBIA Data Retriever | TCIA (and IDC manifests via `.s5cmd`) | CRDC/Gen3 JSON credentials (`--auth`) | skip-existing | MD5 |
| wget, physionet package, aws s3 | PhysioNet | none (open); credentialed login | `wget -c` | `SHA256SUMS.txt` |
| redivis Python client | Stanford AIMI on Redivis | `REDIVIS_API_TOKEN` | n/f | n/f |
| gcapi | Grand Challenge archives | API token | n/f | n/f |
| azcopy | S3 to Azure only | SAS or Entra ID | n/f | n/f |
| BaiduPCS-Go | Baidu Netdisk | BDUSS/STOKEN cookies | n/f | n/f |

- aria2c: "The supported protocols are HTTP(S), FTP, SFTP, BitTorrent, and Metalink". Options include `--checksum`, `-c`, `-x`/`-s` (connections), `-i` with per-URI options including `checksum`, `--header`, `--load-cookies`, `--seed-time`, `--seed-ratio` and `--max-overall-upload-limit` — [aria2c manual](https://aria2.github.io/manual/en/html/aria2c.html).
- rclone hashes: S3 md5, Azure Blob md5, Google Drive md5/sha1/sha256, OneDrive quickxor, Dropbox "dropbox", HTTP none, WebDAV sha1, SFTP md5/sha1, Box sha1, pCloud sha1/sha256, Internet Archive md5/sha1/crc32, Google Cloud Storage md5 — [rclone overview](https://rclone.org/overview/).
- datahugger supports "more than 377 generic and specific (scientific) repositories"; usage is `datahugger <DOI or URL> <folder>` — [datahugger](https://github.com/J535D165/datahugger).
- The sources for the other rows are given in Q1 and Q2: gdown, kaggle, hf, zenodo_get, synapseclient, TDR, tcia_utils, NBIA, PhysioNet, Redivis, gcapi, azcopy and BaiduPCS-Go.

Manual steps for the user, with documented wait times:
- PhysioNet credentialed:
  - Take the CITI "Data or Specimens Only Research" course and upload the training report, not the certificate — [PhysioNet CITI instructions](https://physionet.org/about/citi-course/).
  - Give a reference, who must reply to credentialing@physionet.org. Approval "typically takes 1-2 weeks" (search summary) — [PhysioNet FAQ](https://physionet.org/about/faqs/).
  - 2026-06-18 notice: "applications for credentialed access are likely to be subject to significant delays" because of staffing changes — [PhysioNet delay notice](https://physionet.org/news/post/2026-delay-expected-credentialing/).
  - Then sign the DUA per project, and link an AWS identifier for cloud access (search summaries) — [MIMIC cloud request](https://mimic.mit.edu/docs/gettingstarted/cloud/request).
- TCIA restricted:
  - A DAR through dbGaP, signed by the institution's Signing Official, reviewed by an NIH Data Access Committee, for one year with renewal. Cloud use must be declared — [NIH Universal DUC](https://sharing.nih.gov/sites/default/files/flmngr/Universal_DUC.pdf), [GDC data access policies](https://gdc.cancer.gov/access-data/data-access-policies).
  - No processing time found.
- Stanford AIMI:
  - A Redivis account, then data-access approval by AIMI administrators or completion of "requirements" per dataset — [Redivis access levels](https://docs.redivis.com/reference/data-access/access-levels), [Redivis configuring access](https://docs.redivis.com/reference/data-access/configuring-access).
  - No processing time found.
  - Commercial use: an online application, committee review, a signed licence and the fee — [AIMI commercial use](https://aimi.stanford.edu/datasets-commercial-use).
- Hugging Face gated:
  - A one-time browser request per dataset. Approval is instant (automatic) or manual. The docs' example prompt says "Our team may take 2-3 days to process your request", which is only an example — [HF gated datasets](https://huggingface.co/docs/hub/datasets-gated).
- Kaggle:
  - An account, accepting the rules per competition on the website, and probably phone verification (unverified, forum) — [fast.ai forum](https://forums.fast.ai/t/unable-to-download-bluebook-for-bulldozers-with-kaggle-api/32640).
  - Creating an API token — [Kaggle API docs](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md).
- Synapse:
  - An account (needed for any download). For controlled data, "Request Access", which may need certified or validated status. Validation needs an identity document "current within the past month" — [Synapse account types](https://docs.synapse.org/synapse-docs/synapse-user-account-types).
  - No processing time found.
- Grand Challenge:
  - A human account, one per person. Join the challenge or get archive access. The token is shown once — [Grand Challenge ToS](https://grand-challenge.org/policies/terms-of-service/), [gcapi on PyPI](https://pypi.org/project/gcapi/).
- IEEE DataPort:
  - An IEEE account. A subscription for AWS keys; society members get one free — [IEEE DataPort via AWS](https://ieee-dataport.org/help/accessing-ieee-dataport-dataset-files-through-amazon-web-services-aws), [IEEE DataPort FAQ](https://ieee-dataport.org/faq/how-do-i-access-dataset-ieee-dataport).
- Dryad:
  - An API account from "My account" for higher limits and reliable file downloads (search summary) — [Dryad API](https://datadryad.org/api).
- Google Drive via rclone:
  - Our own OAuth client ID, since the shared one stops working in 2026, or a service account — [rclone drive](https://rclone.org/drive/).
- Baidu:
  - An account (a mainland phone is reportedly needed; unverified), login cookies, and an SVIP purchase for usable speed (unverified) — [BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go), [HF forum post](https://discuss.huggingface.co/t/how-to-download-from-baidu-pan-pan-baidu-com-without-a-chinese-account-2026-notes-for-datasets-a-free-fetcher/180125).

### Inferences
- Start PhysioNet credentialing first, because it is per person and slow. It covers every credentialed PhysioNet project; each project still needs its own DUA signature.
- For TCIA, plan for TDR (CLI) now that NBIA is being phased out. Public DICOM collections that are also in IDC can be copied bucket to bucket instead (see Q3). The IDC overlap is my inference, not verified.
- aria2c with an `-i` list carrying `checksum=` lines is a good common path. It fits Zenodo (feed it `zenodo_get -w`), figshare, Dataverse, Dryad, OSF, CAMUS and PhysioNet open data. Use `--seed-time=0` and an upload limit for torrents on EC2, because seeding uses paid egress (egress cost is my inference).

### Gaps
- No processing times found for dbGaP, Redivis/AIMI, Synapse validation or Grand Challenge archive access.
- Resume behaviour of the kaggle CLI and the Redivis client.
- Whether datahugger checks checksums.

## 7. Proposed tiering, with each host placed

### Takeaway
Tiers:
- A (scriptable, no login): Zenodo, figshare (API), Harvard Dataverse, OSF, PhysioNet open, TCIA open and IDC, the AWS ODR, Hugging Face public, GitHub, CAMUS (Girder), Academic Torrents and direct links on lab sites.
- B (a token or cookie the user supplies once): Kaggle datasets, Synapse open data, Dryad (in practice), IEEE DataPort with a subscription, Google Drive through rclone or gdown cookies, and Hugging Face gated datasets after the one-time request.
- C (a manual step per dataset or competition, then scriptable): Kaggle competitions, Hugging Face gated requests, Stanford AIMI on Redivis, PhysioNet credentialed (per-project DUA, after credentialing), TCIA restricted (dbGaP), Synapse controlled access, Grand Challenge archives or challenges, OneDrive/SharePoint links and Google Drive files over quota.
- D (not automatable): "on request by email", and Baidu Netdisk in practice without a paid account.

### Cited Findings
Table 5. Proposed tier per host, with exceptions. Tier letters: A = no login; B = token or cookie supplied once; C = manual step per dataset or competition, then scriptable; D = not automatable. The evidence column points to the findings above.

| Host | Tier | Exceptions and evidence |
|---|---|---|
| Zenodo | A | Restricted records need a token or request (B or C). Respect the 60/min guest limit and the 2026 bot measures — [Zenodo developers](https://developers.zenodo.org/), [Zenodo blog 2026-01-28](https://blog.zenodo.org/2026/01/28/2026-01-28-improvements-and-support-expectations/) |
| figshare | A | Use the API, not web pages: the web pages showed a WAF challenge (observed) — [figshare API docs](https://docs.figshare.com/) |
| Mendeley Data | A (unverified) | A public API is claimed; the site is behind Cloudflare; restricted datasets would be C — [Mendeley Data archive process](https://data.mendeley.com/archive-process) |
| Kaggle datasets | B | Token once — [Kaggle API docs](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md) |
| Kaggle competitions | C | Accept the rules per competition on the website (plus phone verification, unverified) — [fast.ai forum](https://forums.fast.ai/t/unable-to-download-bluebook-for-bulldozers-with-kaggle-api/32640) |
| Hugging Face public | A | A token is advised against per-IP limits — [HF rate limits](https://huggingface.co/docs/hub/rate-limits) |
| Hugging Face gated | C then B | One browser request per dataset, then a token; authors can revoke — [HF gated datasets](https://huggingface.co/docs/hub/datasets-gated) |
| GitHub | A | LFS-heavy repositories may hit the owner's quota (outside our control); a PAT for API-heavy listing — [GitHub LFS](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-storage-and-bandwidth-usage) |
| Google Drive | B (often C) | gdown with cookies or rclone with our own OAuth client; files over quota need a manual copy to our Drive or a 24 h wait — [Google Drive help](https://support.google.com/drive/answer/2423534?hl=en), [rclone drive](https://rclone.org/drive/) |
| OneDrive / SharePoint | C | No anonymous API for Business or SharePoint; `download=1` sometimes works (unverified) — [Microsoft Graph shares-get](https://learn.microsoft.com/en-us/graph/api/shares-get) |
| Dropbox | A (unverified) | Public links with daily limits on the owner's account — [Dropbox banned links](https://help.dropbox.com/share/banned-links) |
| Baidu Netdisk | D (C with a paid account) | Account, cookies, transfer into own Netdisk, throttled speed — [BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go) |
| Grand Challenge | C | Join or get archive access, then token (B). Much challenge data is on Zenodo or the AWS ODR (A) — [Grand Challenge data storage](https://grand-challenge.org/documentation/data-storage/) |
| TCIA open | A | TDR CLI or IDC buckets — [TDR on GitHub](https://github.com/TCIA/data-retriever), [AWS ODR: IDC](https://registry.opendata.aws/nci-imaging-data-commons/) |
| TCIA restricted | C | dbGaP DAR per project, renewed yearly; then CRDC credentials (B) — [NIH Universal DUC](https://sharing.nih.gov/sites/default/files/flmngr/Universal_DUC.pdf) |
| PhysioNet open | A | wget, physionet package or `aws s3 --no-sign-request` — [PhysioNet PTB-XL page](https://physionet.org/content/ptb-xl/1.0.3/) |
| PhysioNet credentialed | C then B | Credentialing once per person (weeks), DUA per project, then a scripted login — [PhysioNet delay notice](https://physionet.org/news/post/2026-delay-expected-credentialing/) |
| Stanford AIMI (Redivis) | C then B | Approval per dataset, then `REDIVIS_API_TOKEN` — [AIMI shared datasets](https://aimi.stanford.edu/shared-datasets), [Redivis authorization](https://docs.redivis.com/api/rest-api/authorization) |
| Synapse | B (C for controlled) | An account is needed even for open data — [Synapse account types](https://docs.synapse.org/synapse-docs/synapse-user-account-types) |
| IEEE DataPort | B (subscription) or C | Open Access datasets need a login on the website — [IEEE DataPort via AWS](https://ieee-dataport.org/help/accessing-ieee-dataport-dataset-files-through-amazon-web-services-aws) |
| Science Data Bank | A or C (unverified) | Login and conditions on some files; no API docs found — [COAR registry entry](https://ird.coar-repositories.org/systems/b4fe6f36-faa3-474a-9526-e921026c3808?lang=en) |
| Harvard Dataverse | A | Guestbook files add a POST step (still scriptable); restricted files C — [Dataverse Data Access API](https://guides.dataverse.org/en/latest/api/dataaccess.html) |
| Dryad | B | Anonymous file downloads limited or refused (conflicting sources); API account token — [Dryad API](https://datadryad.org/api) |
| OSF | A | A token raises limits — [OSF cookbook](https://ua-libraries-research-data-services.github.io/UALIB_ScholarlyAPI_Cookbook/python/osf.html) |
| Academic Torrents | A | Needs BitTorrent on EC2 (seeding cost; AWS policy not checked) — [Academic Torrents docs](https://academictorrents.com/docs/about.html) |
| AWS ODR | A | Requester-pays buckets need AWS credentials (B) — [S3 Requester Pays](https://docs.aws.amazon.com/AmazonS3/latest/userguide/RequesterPaysBuckets.html) |
| University or lab sites (e.g. CREATIS for CAMUS) | A to C | CAMUS Girder collection is public (observed); other sites may use forms — [Girder collection JSON](https://humanheart-project.creatis.insa-lyon.fr/database/api/v1/collection/6373703d73e9f0047faa1bc8) |
| On request by email | D | Once a link is sent, the host of that link sets the tier (inference) |

### Inferences
- I read "manual step each time" (tier C) as a step per dataset or per competition. In nearly every C case, scripted downloads with a token (B) work after that step.
- A useful second label for the plan is "how long the manual step waits": instant (Hugging Face automatic gates, Kaggle rules), days (Hugging Face manual gates, AIMI, Synapse), or weeks or longer (PhysioNet credentialing in 2026, dbGaP).
- Tier A hosts can still fail from EC2 on bot filters or per-IP limits (Q2). The plan should add one small test per host before scheduling big downloads.

### Gaps
- The placements of Mendeley Data, Dropbox, Science Data Bank and lab websites rest on partial evidence. Each needs one test from the EC2 instance.
- Whether Academic Torrents use on EC2 fits AWS's acceptable use policy was not checked.
