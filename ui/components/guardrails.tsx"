"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Shield, CheckCircle, XCircle } from "lucide-react";
import { PanelSection } from "./panel-section";
import type { GuardrailCheck } from "@/lib/types";

interface GuardrailsProps {
  guardrails: GuardrailCheck[];
  inputGuardrails: string[];
  outputGuardrails: string[];
}

export function Guardrails({ guardrails, inputGuardrails, outputGuardrails }: GuardrailsProps) {
  const guardrailNameMap: Record<string, string> = {
    relevance_guardrail: "Relevance Guardrail",
    jailbreak_guardrail: "Jailbreak Guardrail",
    pii_guardrail: "PII Guardrail",
  };

  const guardrailDescriptionMap: Record<string, string> = {
    "Relevance Guardrail": "Ensure messages are relevant to building and construction",
    "Jailbreak Guardrail":
      "Detect and block attempts to bypass or override system instructions",
    "PII Guardrail":
      "Prevent exposure of Personally Identifiable Information in responses",
  };

  const extractGuardrailName = (rawName: string): string =>
    guardrailNameMap[rawName] ?? rawName;

  // Combine input and output guardrails
  const allGuardrailNames = [
    ...(inputGuardrails || []),
    ...(outputGuardrails || [])
  ];

  const guardrailsToShow: GuardrailCheck[] = allGuardrailNames.map((rawName) => {
    const existing = guardrails.find((gr) => gr.name === rawName);
    if (existing) {
      return existing;
    }
    // Default state for guardrails not yet executed
    return {
      id: rawName,
      name: rawName,
      input: "",
      reasoning: "",
      passed: null, // null means not executed yet
      timestamp: new Date(),
    };
  });

  return (
    <PanelSection
      title="Guardrails"
      icon={<Shield className="h-4 w-4 text-[#928472]" />}
    >
      <div className="grid grid-cols-3 gap-3">
        {guardrailsToShow.map((gr) => {
          // Determine if guardrail has been executed
          const hasExecuted = gr.passed !== null;

          return (
            <Card
              key={gr.id}
              className={`bg-white border-gray-200 transition-all ${
                !hasExecuted ? "opacity-60" : ""
              }`}
            >
              <CardHeader className="p-3 pb-1">
                <CardTitle className="text-sm flex items-center text-zinc-900">
                  {extractGuardrailName(gr.name)}
                </CardTitle>
              </CardHeader>
              <CardContent className="p-3 pt-1">
                <p className="text-xs font-light text-zinc-500 mb-1">
                  {(() => {
                    const title = extractGuardrailName(gr.name);
                    return guardrailDescriptionMap[title] ?? gr.input;
                  })()}
                </p>
                <div className="flex text-xs">
                  {hasExecuted ? (
                    gr.passed ? (
                      <Badge className="mt-2 px-2 py-1 bg-emerald-500 hover:bg-emerald-600 flex items-center text-white">
                        <CheckCircle className="h-4 w-4 mr-1 text-white" />
                        Passed
                      </Badge>
                    ) : (
                      <Badge className="mt-2 px-2 py-1 bg-red-500 hover:bg-red-600 flex items-center text-white">
                        <XCircle className="h-4 w-4 mr-1 text-white" />
                        Failed
                      </Badge>
                    )
                  ) : (
                    <Badge className="mt-2 px-2 py-1 bg-gray-400 hover:bg-gray-500 flex items-center text-white">
                      <CheckCircle className="h-4 w-4 mr-1 text-white" />
                      Pending
                    </Badge>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </PanelSection>
  );
}
