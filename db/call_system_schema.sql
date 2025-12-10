-- 콜 데이터 초안 테이블
CREATE TABLE IF NOT EXISTS call_log (
    call_log_id   BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    call_uuid     VARCHAR(64)  NOT NULL,          -- FreeSWITCH UUID
    direction     ENUM('INBOUND','OUTBOUND') NOT NULL,
    caller        VARCHAR(32)  NOT NULL,          -- 발신번호
    callee        VARCHAR(32)  NOT NULL,          -- 수신번호
    agent_ext     VARCHAR(16)  NULL,              -- 상담원 내선

    started_at    DATETIME(6)  NOT NULL,          -- 다이얼 시작
    ringing_at    DATETIME(6)  NULL,              -- 링잉 시작
    answered_at   DATETIME(6)  NULL,              -- 통화 연결
    ended_at      DATETIME(6)  NOT NULL,          -- 통화 종료

    ring_sec      INT UNSIGNED NOT NULL DEFAULT 0, -- 링잉 시간
    talk_sec      INT UNSIGNED NOT NULL DEFAULT 0, -- 통화 시간(answered~ended)
    total_sec     INT UNSIGNED NOT NULL DEFAULT 0, -- 전체 시간(started~ended)

    hangup_cause  VARCHAR(64) NULL,               -- NORMAL_CLEARING 등

    created_at    DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at    DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),

    KEY idx_call_uuid   (call_uuid),
    KEY idx_started_at  (started_at),
    KEY idx_agent_ext   (agent_ext)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 상담원 초안 테이블 
CREATE TABLE IF NOT EXISTS agent (
    id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    agent_ext       VARCHAR(16) NOT NULL UNIQUE,     -- 내선번호
    agent_name      VARCHAR(50) NOT NULL,            -- 상담원 이름
    password        VARCHAR(255) NULL,               -- 로그인 비밀번호
    is_active       TINYINT(1) DEFAULT 1,            -- 계정 활성 여부

    last_login_at   DATETIME(6) NULL,
    last_logout_at  DATETIME(6) NULL,

    created_at      DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
                        ON UPDATE CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;