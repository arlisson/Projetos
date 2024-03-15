package view;

import java.awt.EventQueue;
import java.awt.Font;
import java.awt.Image;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import java.awt.Color;
import java.awt.Component;
import javax.swing.Box;
import javax.swing.JTable;
import javax.swing.JSeparator;
import javax.swing.SwingConstants;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import org.eclipse.wb.swing.FocusTraversalOnArray;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JTextField;
import javax.swing.JToggleButton;

public class CadastrarProdutor {

	private JFrame frame;
	private JTextField textField;
	private JTextField textField_1;
	private JTextField textField_2;
	private JTextField textField_3;
	private JTextField textField_4;
	private JTextField textField_5;
	private JTextField textField_6;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					CadastrarProdutor window = new CadastrarProdutor();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public CadastrarProdutor() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 800, 584);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);		
			
		JPanel panel = new JPanel();
		panel.setForeground(new Color(67, 79, 32));
		panel.setBackground(new Color(22, 126, 46));
		panel.setBounds(0, 0, 89, 600);
		frame.getContentPane().add(panel);
		
		JButton house = new JButton("");
		house.setBackground(new Color(22, 126, 46));
		house.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\casa.png"));		
		house.setOpaque(false);
        house.setBorderPainted(false);
		panel.add(house);
		
		JButton sino = new JButton("");
		sino.setBackground(new Color(22, 126, 46));
		sino.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\notificacao.png"));
		sino.setOpaque(false);
        sino.setBorderPainted(false);
		panel.add(sino);
		
		JButton calendar = new JButton("");
		calendar.setBackground(new Color(22, 126, 46));
		calendar.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\calendario.png"));
		calendar.setOpaque(false);
		calendar.setBorderPainted(false);
		panel.add(calendar);
		
		JButton graph = new JButton("");
		graph.setBackground(new Color(22, 126, 46));
		graph.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\grafico-para-cima.png"));
		graph.setOpaque(false);
        graph.setBorderPainted(false);
		panel.add(graph);
		
		JButton person = new JButton("");
		person.setBackground(new Color(22, 126, 46));
		person.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\person.png"));
		person.setOpaque(false);
        person.setBorderPainted(false);
		panel.add(person);
		
		JButton config = new JButton("");
		config.setBackground(new Color(22, 126, 46));
		panel.add(config);
		config.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\definicoes.png"));
		config.setOpaque(false);
        config.setBorderPainted(false);
		
		JSeparator separator = new JSeparator();
		separator.setForeground(new Color(0, 0, 0));
		separator.setOrientation(SwingConstants.VERTICAL);
		separator.setBounds(254, 0, 14, 544);
		frame.getContentPane().add(separator);
		
		JButton produtor = new JButton("Produtor");
		produtor.setBackground(new Color(255, 255, 255));
		produtor.setFont(new Font("Tahoma", Font.BOLD, 15));
		produtor.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\menos-do-que-o-simbolo.png"));
		produtor.setBounds(99, 11, 145, 31);
		produtor.setOpaque(false);
        produtor.setBorderPainted(false);
		frame.getContentPane().add(produtor);
		
		JButton adicionar = new JButton("Adicionar");
		adicionar.setForeground(new Color(0, 0, 0));
		adicionar.setBackground(new Color(255, 255, 255));
		adicionar.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\lapis.png"));
		adicionar.setOpaque(false);
        adicionar.setBorderPainted(false);
		adicionar.setFont(new Font("Tahoma", Font.PLAIN, 15));
		adicionar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
			}
		});
		adicionar.setBounds(99, 97, 145, 31);
		frame.getContentPane().add(adicionar);
		
		JButton visualizar = new JButton("Visualizar");
		visualizar.setFont(new Font("Tahoma", Font.PLAIN, 15));
		visualizar.setBackground(new Color(255, 255, 255));
		visualizar.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\celulas.png"));
		visualizar.setOpaque(false);
		visualizar.setBorderPainted(false);
		visualizar.setBounds(99, 168, 145, 31);
		frame.getContentPane().add(visualizar);
		
		JLabel lblNewLabel = new JLabel("Adicionando Produtor");
		lblNewLabel.setFont(new Font("Tahoma", Font.BOLD, 20));
		lblNewLabel.setBounds(278, 11, 248, 60);
		frame.getContentPane().add(lblNewLabel);
		
		JLabel lblNewLabel_1 = new JLabel("Nome Completo");
		lblNewLabel_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1.setBounds(278, 82, 121, 14);
		frame.getContentPane().add(lblNewLabel_1);
		
		textField = new JTextField();
		textField.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField.setBounds(278, 104, 394, 20);
		frame.getContentPane().add(textField);
		textField.setColumns(10);
		
		JLabel lblNewLabel_1_1 = new JLabel("Nome da Mãe");
		lblNewLabel_1_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1_1.setBounds(278, 135, 121, 14);
		frame.getContentPane().add(lblNewLabel_1_1);
		
		textField_1 = new JTextField();
		textField_1.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField_1.setColumns(10);
		textField_1.setBounds(278, 160, 394, 20);
		frame.getContentPane().add(textField_1);
		
		JLabel lblNewLabel_1_1_1 = new JLabel("Nome do Pai");
		lblNewLabel_1_1_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1_1_1.setBounds(278, 191, 121, 14);
		frame.getContentPane().add(lblNewLabel_1_1_1);
		
		textField_2 = new JTextField();
		textField_2.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField_2.setColumns(10);
		textField_2.setBounds(278, 216, 394, 20);
		frame.getContentPane().add(textField_2);
		
		JLabel lblNewLabel_1_1_1_1 = new JLabel("Número de Contato");
		lblNewLabel_1_1_1_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1_1_1_1.setBounds(278, 247, 160, 14);
		frame.getContentPane().add(lblNewLabel_1_1_1_1);
		
		textField_3 = new JTextField();
		textField_3.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField_3.setColumns(10);
		textField_3.setBounds(278, 272, 394, 20);
		frame.getContentPane().add(textField_3);
		
		JLabel lblNewLabel_1_1_1_1_1 = new JLabel("Naturalidade");
		lblNewLabel_1_1_1_1_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1_1_1_1_1.setBounds(278, 303, 121, 14);
		frame.getContentPane().add(lblNewLabel_1_1_1_1_1);
		
		textField_4 = new JTextField();
		textField_4.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField_4.setBounds(278, 328, 184, 20);
		frame.getContentPane().add(textField_4);
		textField_4.setColumns(10);
		
		textField_5 = new JTextField();
		textField_5.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField_5.setColumns(10);
		textField_5.setBounds(488, 328, 184, 20);
		frame.getContentPane().add(textField_5);
		
		JLabel lblNewLabel_1_1_1_1_1_1 = new JLabel("Escolaridade");
		lblNewLabel_1_1_1_1_1_1.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1_1_1_1_1_1.setBounds(488, 304, 121, 14);
		frame.getContentPane().add(lblNewLabel_1_1_1_1_1_1);
		
		JLabel lblNewLabel_1_1_1_1_2 = new JLabel("Data de Nascimento");
		lblNewLabel_1_1_1_1_2.setFont(new Font("Tahoma", Font.PLAIN, 15));
		lblNewLabel_1_1_1_1_2.setBounds(278, 359, 145, 14);
		frame.getContentPane().add(lblNewLabel_1_1_1_1_2);
		
		textField_6 = new JTextField();
		textField_6.setFont(new Font("Tahoma", Font.PLAIN, 12));
		textField_6.setColumns(10);
		textField_6.setBounds(278, 384, 394, 20);
		frame.getContentPane().add(textField_6);
		
		JButton cancelar = new JButton("Cancelar");
		cancelar.setBounds(278, 437, 89, 23);
		frame.getContentPane().add(cancelar);
		
		JButton avancar = new JButton("Cadastrar");
		avancar.setForeground(new Color(255, 255, 255));
		avancar.setBackground(new Color(22, 126, 46));
		avancar.setBounds(387, 437, 100, 23);
		frame.getContentPane().add(avancar);
		
		JButton notificacao = new JButton("");        
		notificacao.setBackground(new Color(255, 255, 255));

        notificacao.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\notificacao.png"));
        notificacao.setOpaque(false);
        notificacao.setBorderPainted(false);
        notificacao.setBounds(643, 20, 38, 43);
        frame.getContentPane().add(notificacao);
		
		JButton user = new JButton("");
		user.setBackground(new Color(255, 255, 255));
		user.setIcon(new ImageIcon("D:\\Users\\T-GAMER\\eclipse-workspace\\Tela\\img\\usuario-de-perfil.png"));
		user.setOpaque(false);
        user.setBorderPainted(false);
		user.setBounds(689, 23, 38, 37);
		frame.getContentPane().add(user);
		
		
	}
}
