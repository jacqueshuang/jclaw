use serde::Serialize;

#[derive(Clone, Serialize)]
pub struct ModuleSummary {
    pub title: String,
    pub value: String,
    pub description: String,
}

#[derive(Clone, Serialize)]
pub struct ConsoleSummary {
    pub skills: ModuleSummary,
    pub channels: ModuleSummary,
    pub agents: ModuleSummary,
}

pub fn default_console_summary() -> ConsoleSummary {
    ConsoleSummary {
        skills: ModuleSummary {
            title: "Skills".into(),
            value: "未配置".into(),
            description: "安装完成后可加载技能市场与本地技能包。".into(),
        },
        channels: ModuleSummary {
            title: "Channel".into(),
            value: "未接入".into(),
            description: "后续可管理聊天渠道接入状态。".into(),
        },
        agents: ModuleSummary {
            title: "Agent".into(),
            value: "0 个实例".into(),
            description: "未来可统一管理 Agent 模板与运行状态。".into(),
        },
    }
}
