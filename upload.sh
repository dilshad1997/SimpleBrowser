

# 🔧 Configuration
GITHUB_USER="dilshad1997"
GITHUB_EMAIL="ahmad.dilshad1997@gmail.com"

REPO_NAME="SimpleBrowser"
PROJECT_PATH="$HOME/SimpleBrowser"

# 📁 Step 1: Project folder create karo (agar nahi hai)
mkdir -p $PROJECT_PATH
cd $PROJECT_PATH

# Example index.html (Flutter ya web app test file)
cat > index.html <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Simple Browser</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 40px;">
  <h1>Simple Browser</h1>
  <form onsubmit="openSite(event)">
    <input id="url" type="text" placeholder="Enter full URL (https://...)" style="width:70%;padding:10px;font-size:16px;">
    <button type="submit" style="padding:10px;">Go</button>
  </form>
  <iframe id="view" src="https://google.com" width="100%" height="600"></iframe>

  <script>
    function openSite(e) {
      e.preventDefault();
      let url = document.getElementById('url').value;
      if (!url.startsWith('http')) url = 'https://' + url;
      document.getElementById('view').src = url;
    }
  </script>
</body>
</html>
EOF

# 🧰 Step 2: Git setup
git init
git config user.name "$GITHUB_USER"
git config user.email "$GITHUB_EMAIL"

# 🧰 Step 3: Create new repo automatically via GitHub API
curl -u "$GITHUB_USER:$GITHUB_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\"}"

# 🧰 Step 4: Push project to GitHub
git add .
git commit -m "Initial Flutter WebView Upload"
git branch -M main
git remote add origin https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git
git push -u origin main

# ✅ Done
echo "🚀 Project successfully uploaded!"
echo "🔗 Repo URL: https://github.com/$GITHUB_USER/$REPO_NAME"

