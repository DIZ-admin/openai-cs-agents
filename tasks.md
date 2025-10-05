# ERNI Gruppe Building Agents - Task List

## Current Focus: Security Hardening & Documentation Refresh

### [x] 1. Security Baseline Verification
- [x] 1.1. Проверить и синхронизировать `SECRET_KEY` и `JWT_SECRET_KEY`
- [x] 1.2. Обновить ProductionSecurityValidator для контроля JWT ключей
- [x] 1.3. Исключить небезопасные дефолты (`changeme`) из docker-compose
- [x] 1.4. Обновить README с перечнем обязательных секретов

### [x] 2. Rate Limiting & Guardrails
- [x] 2.1. Собрать конфигурацию лимитов из `RATE_LIMIT` и `RATE_LIMIT_PER_*`
- [x] 2.2. Убедиться, что `DISABLE_RATE_LIMIT` корректно отключает ограничения
- [x] 2.3. Проверить кэширование input guardrails (Relevance/Jailbreak)
- [x] 2.4. Доработать `faq_lookup_building` с обязательными ссылками

### [x] 3. Документация
- [x] 3.1. Исправить ссылку на `DEPLOYMENT.md` в разделе Support README
- [x] 3.2. Добавить ссылку на `python-backend/docs/ERNI_ADAPTATION.md`
- [x] 3.3. Обновить инструкцию по `.env` (SECRET/JWT/DB/REDIS)
- [x] 3.4. Актуализировать checklist по документации (production checklist)

### [x] 4. Тестирование
- [x] 4.1. Поддерживать сводку тестов (228/228, 90% coverage)
- [x] 4.2. Уточнить статусы тестов в README/tests README (без упоминания провалов)
- [x] 4.3. Освежить задачи на регрессию и интеграцию (pytest, e2e)

### [x] 5. Следующие шаги
- [x] 5.1. Подготовить production docker-compose с защищёнными переменными (`docker-compose.prod.yml`)
- [x] 5.2. Добавить автоматическую проверку секретов в CI (pre-start smoke test)
- [x] 5.3. Подготовить инструкции по ротации ключей (README/Runbook)
- [x] 5.4. Обновить RUNBOOK.md пошаговыми скриптами запуска Docker (production)

## Notes
- Environment: macOS (Darwin)
- Python: 3.9.6
- Node.js: v23.11.0
- Branch: staging
- Следующие приоритеты: CI проверка секретов, политика ротации ключей, дополнения к runbook
