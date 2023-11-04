module if_neuron(
    input wire clk,
    input wire rst_n,
    input wire[15:0] spike_current,
    output reg spike
);

    parameter THRESHOLD = 16'h0100;
    parameter RESET_CURRENT = 16'h0000;

    reg [15:0] accumulated_current;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            accumulated_current <= RESET_CURRENT;
            spike <= 1'b0;
        end else begin
            accumulated_current <= accumulated_current + spike_current;

            if (accumulated_current >= THRESHOLD) begin
                spike <= 1'b1;
                accumulated_current <= RESET_CURRENT; 
            end else begin
                spike <= 1'b0;
            end
        end
    end

endmodule


module tt_um_manjushettar(
    input  wire [7:0] ui_in,
    output wire [7:0] uo_out,
    input  wire [7:0] uio_in,
    output wire [7:0] uio_out,
    output wire [7:0] uio_oe,
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

    wire spike1_1, spike1_2;
    reg [15:0] input2_1, input2_2;

    if_neuron neuron1_1 (
        .clk(clk),
        .rst_n(rst_n),
        .spike_current({8'h00, ui_in}),
        .spike(spike1_1)
    );

    if_neuron neuron1_2 (
        .clk(clk),
        .rst_n(rst_n),
        .spike_current({8'h00, uio_in}), 
        .spike(spike1_2)
    );

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            input2_1 <= 16'h0000;
            input2_2 <= 16'h0000;
        end else begin
            input2_1 <= spike1_1 ? 16'hFFFF : 16'h0000;
            input2_2 <= spike1_2 ? 16'hFFFF : 16'h0000;
        end
    end

    wire spike2_1, spike2_2;

    if_neuron neuron2_1 (
        .clk(clk),
        .rst_n(rst_n),
        .spike_current(input2_1),
        .spike(spike2_1)
    );

    if_neuron neuron2_2 (
        .clk(clk),
        .rst_n(rst_n),
        .spike_current(input2_2),
        .spike(spike2_2)
    );

    assign uo_out = {6'b000000, spike2_2, spike2_1};

    assign uio_out = 8'b00000000;
    assign uio_oe = 8'b00000000;


endmodule

