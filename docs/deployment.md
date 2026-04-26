# nvlink.lol 部署说明

## 部署映射

- GitHub repository: `gateszhangc/nvlink`
- Git branch: `main`
- Image repository: `registry.144.91.77.245.sslip.io/nvlink`
- K8s manifest path: `deploy/k8s/overlays/prod`
- Argo CD application: `nvlink`
- Primary domain: `nvlink.lol`
- Argo platform repo: `gateszhangc/argo-platform`
- Dokploy project: `n/a`，本项目按要求不使用 Dokploy
- Preview URL: `https://nvlink.144.91.77.245.sslip.io/`

发布链路：

`gateszhangc/nvlink -> main -> registry.144.91.77.245.sslip.io/nvlink -> deploy/k8s/overlays/prod -> Argo CD application nvlink`

## 当前仓库内的发布骨架

- GitHub Actions: `.github/workflows/build-and-release.yml`
- K8s build job 模板: `deploy/build/image-build-job.yaml`
- Kustomize prod overlay: `deploy/k8s/overlays/prod/kustomization.yaml`
- Argo CD 资源: `deploy/argocd/application.yaml` 与 `deploy/argocd/appproject.yaml`

## 发布流程

1. GitHub Actions 在 `main` 分支 push 后触发。
2. workflow 使用 `kubectl` 连接集群，创建临时 build job。
3. build job 在 Kubernetes 中用 Kaniko 拉取当前仓库指定 commit，构建镜像并推送到 `registry.144.91.77.245.sslip.io/nvlink:<git-sha>`。
4. workflow 将 `deploy/k8s/overlays/prod/kustomization.yaml` 里的 `images[].newTag` 回写为本次 `git sha`。
5. workflow 提交一条 `chore: release nvlink <sha> [skip ci]` 到 `main`。
6. Argo CD 监控 `deploy/k8s/overlays/prod`，发现 `newTag` 变化后自动同步。
7. Ingress 将 `www.nvlink.lol` 308 跳转到 `https://nvlink.lol`。

## 首次初始化清单

1. 创建新仓库 `gateszhangc/nvlink` 并推送当前代码。
2. 给新仓库写入 secrets：
   - `KUBE_CONFIG_DATA`
   - `REGISTRY_USERNAME`
   - `REGISTRY_PASSWORD`
   - `K8S_BUILD_GIT_TOKEN`（可选，不设时回退到 `github.token`）
3. 在集群执行：
   - `kubectl apply -f deploy/argocd/appproject.yaml`
   - `kubectl apply -f deploy/argocd/application.yaml`
4. 将域名 `nvlink.lol` 托管到 Cloudflare，并将 apex / www 指向集群入口。
5. 站点可访问后，将 `sc-domain:nvlink.lol` 接入 Google Search Console，并提交 `https://nvlink.lol/sitemap.xml`。

## 2026-04-26 当前状态

- GitHub Actions `Build And Release` 已成功跑通，集群内 Kaniko 构建和 `newTag` 回写正常。
- Argo CD Application `nvlink` 当前为 `Synced` + `Healthy`。
- `nvlink` 工作负载 pod 已 ready。
- Cloudflare zone `nvlink.lol` 已创建，当前 nameserver 为：
  - `jaziel.ns.cloudflare.com`
  - `sandra.ns.cloudflare.com`
- Cloudflare zone 中已写入以下 DNS-only A 记录：
  - `nvlink.lol -> 144.91.73.228`
  - `nvlink.lol -> 144.91.77.245`
  - `nvlink.lol -> 144.91.78.201`
  - `www.nvlink.lol -> 144.91.73.228`
  - `www.nvlink.lol -> 144.91.77.245`
  - `www.nvlink.lol -> 144.91.78.201`
- 当前阻塞点：Porkbun 账户未开启 domain API access，脚本无法自动把注册商 nameserver 从 Porkbun 切到 Cloudflare。
- 在 Porkbun 面板把 nameserver 手动切到上面的两个 Cloudflare NS 后，主域名证书签发、GSC 验证和最终线上验收即可继续。

## 验收标准

- `https://nvlink.lol/` 可访问
- `https://www.nvlink.lol/` 正确跳转到 apex
- Argo CD Application `nvlink` 状态为 `Healthy` 且 `Synced`
- 首页图片、favicon、manifest 可正常加载
- GSC 中 `sc-domain:nvlink.lol` 已可见并列出 sitemap
