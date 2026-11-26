# 8. Upload, approval and cross-posting

Everything goes through **n8n** at `https://n8n.cobaltsoft.eu` (the owner's instance). All upload webhooks require the header `x-upload-token`; the token is **not** in this repo. Read it from the workflow's webhook settings in n8n (via the n8n MCP `get_workflow_details`) or ask the owner.

## Workflows

| Workflow (id) | Webhook | What it does |
|---|---|---|
| Upload endpoint (`7tyD8HLjJizSmv8L`) | `POST /webhook/unlikelyyou-upload` multipart: `data`=file, `title`, `description`, `tags`, `privacy` (default private) | Simple upload for small files. Returns `{uploadId}`. |
| Large video upload (`LVY18O9nVN6a51iQ`) | `POST /webhook/unlikelyyou-start` JSON `{title, description, tags, size}` then `POST /webhook/unlikelyyou-chunk` multipart `data, session, start, end, total` in 8 MB chunks | Resumable upload for long videos. |
| Review (`klNaeQNGf8lnkU0s`) | `POST /webhook/unlikelyyou-review` `data, title, description, tags, publishAt` | Uploads private, sends a Telegram message with **Publish / Hold** buttons, then schedules. Use for Shorts. |
| Approve + pick thumbnail (`J6UX0j4yk4sgvfST`) | `POST /webhook/unlikelyyou-approve` `videoId, title, description, tags, publishAt, thumbA/B/C` | Sends 3 thumbnails to Telegram, owner picks A/B/C, then Publish/Hold. Use for long videos after the chunk upload. |
| Schedule utility (`aS6W4ex4zL5NYYlY`) | `/webhook/unlikelyyou-schedule {videoId, publishAt?}` (omit = unschedule), `/webhook/unlikelyyou-ask-schedule` | Change or ask for a publish time. |
| Homepage/privacy (`9JRQZcL1leai8OgC`) | `/webhook/unlikelyyou`, `/webhook/unlikelyyou-privacy` | Needed by the Google OAuth app. **Keep active.** |
| Set banner (`ad4ODbcS5tBoYxRK`, inactive) | | Activate to change the banner. |

n8n credentials: "YouTube - The Unlikely You" (OAuth), "Telegram - channel" (the channel bot, owner's chat). Telegram messages use Markdown, so **escape underscores** in video ids and titles.

## Flow for a finished episode

1. Render long video + parts + 3 thumbnails.
2. Long video: chunk upload (private) then `unlikelyyou-approve` with the thumbnails and a planned publish time.
3. Parts as Shorts: `unlikelyyou-review` each, with publish times.
4. The owner taps Publish/Hold in Telegram. Nothing goes public without that tap.
5. Default settings: made for kids = **false**, synthetic/altered-content label **off** (clearly animated fiction), category Entertainment.
6. Preferred publish time: about **19:00 Sofia time** (17:00 UTC in winter).

## Limits and known issues

- Unverified channel: ~10 uploads per day (`uploadLimitExceeded`), no custom thumbnails, no clickable outside links. Phone verification has been failing for the owner; the long "Everyone Vanished" video waits until it works.
- Instagram: the official API can post Reels to the owner's professional account through their own Meta app (needs a public video URL). TikTok's Direct Post API is private-only without an audit, so use an approved scheduler (Buffer/Metricool) or post manually. **No browser bots.**
- Public posts written for the owner (captions, replies) should sound casual and human, not AI-polished.
